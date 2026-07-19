import {
  useMemo,
  useRef,
  useState,
  type DragEvent as ReactDragEvent,
  type MouseEvent as ReactMouseEvent,
  type PointerEvent as ReactPointerEvent,
} from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  ArrowUpDown,
  BedDouble,
  DoorOpen,
  Footprints,
  GitBranch,
  Loader2,
  MapPinned,
  MousePointer2,
  Presentation,
  RefreshCw,
  Save,
  Trash2,
  TrendingUp,
  Unlink,
  type LucideIcon,
} from 'lucide-react'
import {
  assignRoomToIndoorNode,
  createIndoorEdge,
  createIndoorNode,
  deleteIndoorEdge,
  deleteIndoorNode,
  getIndoorNavigationGraph,
  resetIndoorNavigationGraph,
  updateIndoorNode,
} from '../../../entities/indoor-navigation/api/indoor-navigation-api'
import type {
  IndoorNavigationGraph,
  IndoorNodeType,
  IndoorRouteNode,
} from '../../../entities/indoor-navigation/model/indoor-navigation.schemas'
import { ApiError } from '../../../shared/api/http-client'
import type { RoomSnapshot } from '../model/simulation.schemas'
import './indoor-map-editor.css'

const indoorGraphQueryKey = ['indoor-navigation-graph'] as const
const nodeTypeLabels: Record<IndoorNodeType, string> = {
  CORRIDOR: 'Hành lang',
  DOOR: 'Cửa phòng',
  STAIRS: 'Cầu thang',
  ELEVATOR: 'Thang máy',
  ENTRANCE: 'Lối vào',
}

interface NodePaletteItem {
  key: string
  label: string
  nodeType: IndoorNodeType
  Icon: LucideIcon
}

const nodePalette: NodePaletteItem[] = [
  { key: 'corridor', label: 'Hành lang', nodeType: 'CORRIDOR', Icon: Footprints },
  { key: 'room', label: 'Phòng bệnh', nodeType: 'DOOR', Icon: BedDouble },
  { key: 'hall', label: 'Hội trường', nodeType: 'DOOR', Icon: Presentation },
  { key: 'stairs', label: 'Cầu thang', nodeType: 'STAIRS', Icon: TrendingUp },
  { key: 'elevator', label: 'Thang máy', nodeType: 'ELEVATOR', Icon: ArrowUpDown },
  { key: 'entrance', label: 'Lối vào', nodeType: 'ENTRANCE', Icon: DoorOpen },
]

type EditorStep = 'nodes' | 'edges'
type GraphAction =
  | { type: 'create-node'; payload: Parameters<typeof createIndoorNode>[0] }
  | {
      type: 'update-node'
      nodeId: string
      payload: Parameters<typeof updateIndoorNode>[1]
    }
  | { type: 'delete-node'; nodeId: string }
  | { type: 'create-edge'; payload: Parameters<typeof createIndoorEdge>[0] }
  | { type: 'delete-edge'; edgeId: string }
  | { type: 'assign-room'; roomCode: string; nodeId: string | null }
  | { type: 'reset' }

function executeGraphAction(action: GraphAction): Promise<IndoorNavigationGraph> {
  switch (action.type) {
    case 'create-node':
      return createIndoorNode(action.payload)
    case 'update-node':
      return updateIndoorNode(action.nodeId, action.payload)
    case 'delete-node':
      return deleteIndoorNode(action.nodeId)
    case 'create-edge':
      return createIndoorEdge(action.payload)
    case 'delete-edge':
      return deleteIndoorEdge(action.edgeId)
    case 'assign-room':
      return assignRoomToIndoorNode(action.roomCode, action.nodeId)
    case 'reset':
      return resetIndoorNavigationGraph()
  }
}

function pointFromEvent(
  event: { clientX: number; clientY: number },
  element: HTMLElement,
) {
  const bounds = element.getBoundingClientRect()
  return {
    xPercent: Math.min(
      100,
      Math.max(0, ((event.clientX - bounds.left) / bounds.width) * 100),
    ),
    yPercent: Math.min(
      100,
      Math.max(0, ((event.clientY - bounds.top) / bounds.height) * 100),
    ),
  }
}

function normalizeRoomCode(value: string) {
  return value.toUpperCase().trim()
}

function connectorSuffix(node: IndoorRouteNode) {
  return node.connectorCode?.split('_').at(-1)
}

interface IndoorMapEditorPanelProps {
  rooms: RoomSnapshot[]
}

export function IndoorMapEditorPanel({ rooms }: IndoorMapEditorPanelProps) {
  const queryClient = useQueryClient()
  const mapRef = useRef<HTMLDivElement>(null)
  const movedDuringDragRef = useRef(false)
  const [floorId, setFloorId] = useState('')
  const [editorStep, setEditorStep] = useState<EditorStep>('nodes')
  const [paletteKey, setPaletteKey] = useState(nodePalette[0].key)
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null)
  const [linkFromNodeId, setLinkFromNodeId] = useState<string | null>(null)
  const [editName, setEditName] = useState('')
  const [selectedRoomCode, setSelectedRoomCode] = useState('')
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [dragging, setDragging] = useState<{
    nodeId: string
    xPercent: number
    yPercent: number
    startX: number
    startY: number
  }>()

  const graphQuery = useQuery({
    queryKey: indoorGraphQueryKey,
    queryFn: getIndoorNavigationGraph,
  })
  const mutation = useMutation({
    mutationFn: executeGraphAction,
    onSuccess: (graph, action) => {
      queryClient.setQueryData(indoorGraphQueryKey, graph)
      setError(null)
      if (action.type === 'create-node') {
        setMessage(
          action.payload.type === 'STAIRS' || action.payload.type === 'ELEVATOR'
            ? 'Đã tạo điểm và tự đồng bộ trục liên tầng A/B/C.'
            : 'Đã tạo node định vị và lưu vào cơ sở dữ liệu.',
        )
      }
      if (action.type === 'update-node') {
        setMessage('Đã cập nhật node trong cơ sở dữ liệu.')
      }
      if (action.type === 'delete-node') {
        setMessage('Đã xóa node và các cạnh liên quan.')
      }
      if (action.type === 'create-edge') {
        setMessage('Đã nối và lưu edge giữa hai node.')
      }
      if (action.type === 'delete-edge') setMessage('Đã xóa edge.')
      if (action.type === 'assign-room') {
        setMessage('Đã cập nhật ánh xạ phòng vào node.')
      }
      if (action.type === 'reset') setMessage('Đã khôi phục sơ đồ mặc định.')
    },
    onError: () => {
      setError(
        'Không lưu được thay đổi. Dữ liệu có thể trùng hoặc vi phạm quy tắc nối tầng.',
      )
    },
  })

  const graph = graphQuery.data
  const effectiveFloorId = floorId || graph?.floors[0]?.id || ''
  const effectiveRoomCode = selectedRoomCode || rooms[0]?.location_code || ''
  const floor = graph?.floors.find((item) => item.id === effectiveFloorId)
  const floorNodes = useMemo(
    () =>
      graph?.nodes.filter((node) => node.floorId === effectiveFloorId) ?? [],
    [effectiveFloorId, graph],
  )
  const floorEdges = useMemo(
    () =>
      graph?.edges.filter(
        (edge) => edge.floorId === effectiveFloorId && !edge.isInterFloor,
      ) ?? [],
    [effectiveFloorId, graph],
  )
  const selectedNode = graph?.nodes.find((node) => node.id === selectedNodeId)
  const displayedNodes = floorNodes.map((node) =>
    dragging?.nodeId === node.id
      ? { ...node, xPercent: dragging.xPercent, yPercent: dragging.yPercent }
      : node,
  )
  const nodeById = new Map(graph?.nodes.map((node) => [node.id, node]) ?? [])
  const floorById = new Map(graph?.floors.map((item) => [item.id, item]) ?? [])
  const connectorNodes = floorNodes.filter((node) => node.connectorCode)
  const interFloorEdges = graph?.edges.filter((edge) => edge.isInterFloor) ?? []
  const interFloorEdgesForFloor = interFloorEdges.filter((edge) => {
    const source = nodeById.get(edge.fromNodeId)
    const target = nodeById.get(edge.toNodeId)
    return source?.floorId === effectiveFloorId || target?.floorId === effectiveFloorId
  })
  const currentAssignment = graph?.roomAssignments.find((assignment) => {
    const assignmentCode = normalizeRoomCode(assignment.roomCode)
    const roomCode = normalizeRoomCode(effectiveRoomCode)
    const assignmentNumber = assignmentCode.match(/\d{3}/)?.[0]
    const roomNumber = roomCode.match(/\d{3}/)?.[0]
    return (
      assignmentCode === roomCode ||
      Boolean(assignmentNumber && assignmentNumber === roomNumber)
    )
  })

  function selectNodeForEditing(nodeId: string) {
    const node = graph?.nodes.find((item) => item.id === nodeId)
    setSelectedNodeId(nodeId)
    setEditName(node?.name ?? '')
  }

  function placePaletteItem(
    event: { clientX: number; clientY: number },
    requestedPaletteKey = paletteKey,
  ) {
    if (
      editorStep !== 'nodes' ||
      !floor ||
      !mapRef.current ||
      mutation.isPending
    ) {
      return
    }
    const item = nodePalette.find((option) => option.key === requestedPaletteKey)
    if (!item) return
    const point = pointFromEvent(event, mapRef.current)
    const nextNumber =
      floorNodes.filter((node) => node.name.startsWith(item.label)).length + 1
    mutation.mutate({
      type: 'create-node',
      payload: {
        floorId: floor.id,
        name: `${item.label} ${nextNumber}`,
        type: item.nodeType,
        ...point,
      },
    })
  }

  function addNodeAtMap(event: ReactMouseEvent<HTMLDivElement>) {
    placePaletteItem(event)
  }

  function dropPaletteItem(event: ReactDragEvent<HTMLDivElement>) {
    if (editorStep !== 'nodes') return
    event.preventDefault()
    const requestedPaletteKey =
      event.dataTransfer.getData('application/x-indoor-node') || paletteKey
    placePaletteItem(event, requestedPaletteKey)
  }

  function beginDrag(
    event: ReactPointerEvent<HTMLButtonElement>,
    nodeId: string,
  ) {
    const node = displayedNodes.find((item) => item.id === nodeId)
    if (!node) return
    event.stopPropagation()
    selectNodeForEditing(nodeId)
    if (editorStep !== 'nodes') return
    event.currentTarget.setPointerCapture(event.pointerId)
    movedDuringDragRef.current = false
    setDragging({
      nodeId,
      xPercent: node.xPercent,
      yPercent: node.yPercent,
      startX: node.xPercent,
      startY: node.yPercent,
    })
  }

  function moveNode(event: ReactPointerEvent<HTMLDivElement>) {
    if (!dragging || !mapRef.current) return
    const point = pointFromEvent(event, mapRef.current)
    if (
      Math.abs(point.xPercent - dragging.startX) > 0.15 ||
      Math.abs(point.yPercent - dragging.startY) > 0.15
    ) {
      movedDuringDragRef.current = true
    }
    setDragging((current) => (current ? { ...current, ...point } : current))
  }

  function finishDrag() {
    if (!dragging) return
    if (movedDuringDragRef.current) {
      mutation.mutate({
        type: 'update-node',
        nodeId: dragging.nodeId,
        payload: {
          xPercent: Number(dragging.xPercent.toFixed(2)),
          yPercent: Number(dragging.yPercent.toFixed(2)),
        },
      })
    }
    setDragging(undefined)
  }

  function selectOrConnectNode(nodeId: string) {
    if (movedDuringDragRef.current) {
      movedDuringDragRef.current = false
      return
    }
    selectNodeForEditing(nodeId)
    if (editorStep !== 'edges') {
      setLinkFromNodeId(null)
      return
    }
    if (!linkFromNodeId) {
      setLinkFromNodeId(nodeId)
      setMessage('Đã chọn node đầu. Bấm node thứ hai để nối edge.')
      return
    }
    if (linkFromNodeId === nodeId) {
      setLinkFromNodeId(null)
      setMessage('Đã bỏ chọn node đầu.')
      return
    }
    mutation.mutate({
      type: 'create-edge',
      payload: {
        fromNodeId: linkFromNodeId,
        toNodeId: nodeId,
        type: 'CORRIDOR',
      },
    })
    setLinkFromNodeId(null)
  }

  function switchToEdges() {
    if (floorNodes.length < 2) {
      setMessage('Tầng này cần ít nhất 2 node trước khi nối edge.')
      return
    }
    setEditorStep('edges')
    setSelectedNodeId(null)
    setLinkFromNodeId(null)
    setMessage('Bấm node đầu rồi bấm node thứ hai để tạo edge.')
  }

  function connectorFloorNames(node: IndoorRouteNode) {
    return (
      graph?.nodes
        .filter(
          (item) =>
            item.type === node.type && item.connectorCode === node.connectorCode,
        )
        .sort(
          (left, right) =>
            (floorById.get(left.floorId)?.floorNumber ?? 0) -
            (floorById.get(right.floorId)?.floorNumber ?? 0),
        )
        .map((item) => floorById.get(item.floorId)?.name)
        .filter(Boolean)
        .join(' ↕ ') ?? ''
    )
  }

  if (graphQuery.isPending) {
    return (
      <div className="sim-map-state">
        <Loader2 className="is-spinning" /> Đang tải sơ đồ từ cơ sở dữ liệu…
      </div>
    )
  }
  if (graphQuery.isError || !graph) {
    const isBackendVersionMissing =
      graphQuery.error instanceof ApiError && graphQuery.error.status === 404
    return (
      <div className="sim-map-state is-error" role="alert">
        <p>
          {isBackendVersionMissing
            ? 'Backend đang chạy chưa có API sơ đồ chỉ đường. Hãy triển khai phiên bản backend mới rồi tải lại trang.'
            : 'Không tải được sơ đồ chỉ đường từ backend. Hãy kiểm tra kết nối máy chủ rồi thử lại.'}
        </p>
        <button type="button" onClick={() => graphQuery.refetch()}>
          <RefreshCw size={16} /> Thử lại
        </button>
      </div>
    )
  }

  return (
    <div className="sim-map-editor">
      <section className="sim-map-editor__intro">
        <div>
          <span>SƠ ĐỒ ĐANG DÙNG THẬT</span>
          <h2>Chỉnh mạng đường đi của bệnh viện</h2>
          <p>
            Đặt node bằng kéo-thả, nối edge theo từng tầng. Cầu thang và thang
            máy cùng trục A/B/C được tự nối giữa hai tầng liền kề.
          </p>
        </div>
        <div className="sim-map-version">
          <small>PHIÊN BẢN</small>
          <strong>v{graph.version}</strong>
          <button
            type="button"
            onClick={() => {
              if (window.confirm('Khôi phục toàn bộ node và edge mặc định?')) {
                mutation.mutate({ type: 'reset' })
              }
            }}
            disabled={mutation.isPending}
          >
            <RefreshCw size={15} /> Khôi phục mặc định
          </button>
        </div>
      </section>

      {message && (
        <p className="sim-message" role="status" onClick={() => setMessage(null)}>
          {message}
        </p>
      )}
      {error && (
        <p className="sim-message is-error" role="alert" onClick={() => setError(null)}>
          {error}
        </p>
      )}

      <div className="sim-map-editor__workspace">
        <section className="sim-map-board">
          <div className="sim-editor-step-tabs" aria-label="Các bước cấu hình đường đi">
            <button
              type="button"
              className={editorStep === 'nodes' ? 'is-active' : ''}
              onClick={() => {
                setEditorStep('nodes')
                setLinkFromNodeId(null)
              }}
            >
              1. Đặt node
            </button>
            <button
              type="button"
              className={editorStep === 'edges' ? 'is-active' : ''}
              disabled={floorNodes.length < 2}
              onClick={switchToEdges}
            >
              2. Nối edge
            </button>
          </div>

          <div className="sim-map-toolbar is-compact">
            <label>
              <span>Tầng đang chỉnh</span>
              <select
                value={effectiveFloorId}
                onChange={(event) => {
                  const nextFloorId = event.target.value
                  const nextFloorNodeCount = graph.nodes.filter(
                    (node) => node.floorId === nextFloorId,
                  ).length
                  setFloorId(nextFloorId)
                  setSelectedNodeId(null)
                  setLinkFromNodeId(null)
                  if (editorStep === 'edges' && nextFloorNodeCount < 2) {
                    setEditorStep('nodes')
                    setMessage(
                      'Tầng mới chưa đủ 2 node nên đã quay về bước đặt node.',
                    )
                  }
                }}
              >
                {graph.floors.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.name}
                  </option>
                ))}
              </select>
            </label>
            <div className="sim-floor-summary">
              <span>{floorNodes.length} node</span>
              <span>{floorEdges.length} edge</span>
              <span>{connectorNodes.length} điểm liên tầng</span>
            </div>
          </div>

          {editorStep === 'nodes' && (
            <div className="sim-node-palette" aria-label="Khay loại node">
              {nodePalette.map((item) => {
                const Icon = item.Icon
                return (
                  <button
                    key={item.key}
                    type="button"
                    draggable
                    className={paletteKey === item.key ? 'is-active' : ''}
                    onClick={() => setPaletteKey(item.key)}
                    onDragStart={(event) => {
                      setPaletteKey(item.key)
                      event.dataTransfer.setData(
                        'application/x-indoor-node',
                        item.key,
                      )
                      event.dataTransfer.effectAllowed = 'copy'
                    }}
                    title={`Kéo ${item.label} lên sơ đồ`}
                  >
                    <Icon size={18} />
                    <span>{item.label}</span>
                  </button>
                )
              })}
            </div>
          )}

          <div className="sim-map-help">
            <MousePointer2 size={16} />
            {editorStep === 'nodes'
              ? 'Kéo biểu tượng thả lên sơ đồ, hoặc chọn biểu tượng rồi bấm vị trí. Kéo node để sửa tọa độ.'
              : 'Bấm node đầu rồi node thứ hai để nối. Bấm đường xanh để xóa edge.'}
          </div>

          {floor ? (
            <div
              ref={mapRef}
              className={`sim-map-canvas ${
                editorStep === 'nodes' ? 'is-adding' : 'is-linking-step'
              }`}
              style={{ aspectRatio: `${floor.mapWidth}/${floor.mapHeight}` }}
              onClick={addNodeAtMap}
              onDragOver={(event) => {
                if (editorStep === 'nodes') {
                  event.preventDefault()
                  event.dataTransfer.dropEffect = 'copy'
                }
              }}
              onDrop={dropPaletteItem}
              onPointerMove={moveNode}
              onPointerUp={finishDrag}
              onPointerCancel={finishDrag}
            >
              <img src={floor.mapImageUrl} alt={`Sơ đồ ${floor.name}`} />
              <svg
                viewBox={`0 0 ${floor.mapWidth} ${floor.mapHeight}`}
                preserveAspectRatio="none"
                aria-label="Các edge đã lưu"
              >
                {floorEdges.map((edge) => {
                  const source = displayedNodes.find(
                    (node) => node.id === edge.fromNodeId,
                  )
                  const target = displayedNodes.find(
                    (node) => node.id === edge.toNodeId,
                  )
                  return source && target ? (
                    <line
                      key={edge.id}
                      x1={(source.xPercent * floor.mapWidth) / 100}
                      y1={(source.yPercent * floor.mapHeight) / 100}
                      x2={(target.xPercent * floor.mapWidth) / 100}
                      y2={(target.yPercent * floor.mapHeight) / 100}
                      onClick={(event) => {
                        event.stopPropagation()
                        if (window.confirm('Xóa edge này?')) {
                          mutation.mutate({
                            type: 'delete-edge',
                            edgeId: edge.id,
                          })
                        }
                      }}
                    >
                      <title>Bấm để xóa edge</title>
                    </line>
                  ) : null
                })}
              </svg>
              {displayedNodes.map((node, index) => (
                <button
                  key={node.id}
                  type="button"
                  className={`sim-route-node is-${node.type.toLowerCase()} ${
                    selectedNodeId === node.id ? 'is-selected' : ''
                  } ${linkFromNodeId === node.id ? 'is-linking' : ''}`}
                  style={{ left: `${node.xPercent}%`, top: `${node.yPercent}%` }}
                  title={`${node.name} — ${
                    editorStep === 'nodes' ? 'kéo để đổi vị trí' : 'bấm để nối edge'
                  }`}
                  onPointerDown={(event) => beginDrag(event, node.id)}
                  onClick={(event) => {
                    event.stopPropagation()
                    selectOrConnectNode(node.id)
                  }}
                >
                  {connectorSuffix(node) ?? index + 1}
                </button>
              ))}
            </div>
          ) : (
            <div className="sim-map-empty">Chưa có dữ liệu tầng.</div>
          )}
        </section>

        <aside className="sim-map-inspector">
          <section>
            <h3>
              <MapPinned size={17} /> Node đang chọn
            </h3>
            {selectedNode ? (
              <>
                {selectedNode.connectorCode ? (
                  <div className="sim-connector-identity">
                    <strong>{selectedNode.name}</strong>
                    <span>Trục {connectorSuffix(selectedNode)} được quản lý tự động</span>
                  </div>
                ) : (
                  <label>
                    <span>Tên hiển thị</span>
                    <input
                      value={editName}
                      onChange={(event) => setEditName(event.target.value)}
                    />
                  </label>
                )}
                <p className="sim-node-coordinates">
                  {nodeTypeLabels[selectedNode.type]} · X{' '}
                  {selectedNode.xPercent.toFixed(2)}% · Y{' '}
                  {selectedNode.yPercent.toFixed(2)}%
                </p>
                {!selectedNode.connectorCode && (
                  <button
                    type="button"
                    className="is-primary"
                    disabled={!editName.trim() || editName.trim() === selectedNode.name}
                    onClick={() =>
                      mutation.mutate({
                        type: 'update-node',
                        nodeId: selectedNode.id,
                        payload: { name: editName.trim() },
                      })
                    }
                  >
                    <Save size={15} /> Lưu tên
                  </button>
                )}
                <button
                  type="button"
                  className="is-danger"
                  onClick={() => {
                    if (window.confirm(`Xóa node “${selectedNode.name}”?`)) {
                      mutation.mutate({
                        type: 'delete-node',
                        nodeId: selectedNode.id,
                      })
                      setSelectedNodeId(null)
                      setLinkFromNodeId(null)
                    }
                  }}
                >
                  <Trash2 size={15} /> Xóa node
                </button>
              </>
            ) : (
              <p className="sim-map-muted">
                Bấm một node trên sơ đồ để xem hoặc chỉnh sửa.
              </p>
            )}
          </section>

          <section className="sim-connector-shafts">
            <h3>
              <ArrowUpDown size={17} /> Trục liên tầng tự động
            </h3>
            <p className="sim-map-muted">
              Cầu thang và thang máy cùng chữ A/B/C được tự nối giữa hai tầng
              liền kề. Hệ thống chặn nối chéo hai trục.
            </p>
            {connectorNodes.length === 0 ? (
              <p className="sim-map-muted">Tầng này chưa có điểm liên tầng.</p>
            ) : (
              connectorNodes.map((node) => (
                <div key={node.id}>
                  <strong>{node.name}</strong>
                  <small>{connectorFloorNames(node)}</small>
                </div>
              ))
            )}
            <p className="sim-connector-edge-count">
              {interFloorEdgesForFloor.length} kết nối sang tầng liền kề
            </p>
          </section>

          {editorStep === 'nodes' && (
            <section>
              <h3>
                <MapPinned size={17} /> Gán phòng vào node cửa
              </h3>
              <label>
                <span>Phòng chức năng</span>
                <select
                  value={effectiveRoomCode}
                  onChange={(event) => setSelectedRoomCode(event.target.value)}
                >
                  {rooms.map((room) => (
                    <option key={room.code} value={room.location_code}>
                      {room.location_code} · {room.name}
                    </option>
                  ))}
                </select>
              </label>
              <div className="sim-assignment-status">
                <span>Đang gán vào</span>
                <strong>
                  {currentAssignment
                    ? nodeById.get(currentAssignment.nodeId)?.name ??
                      'Node đã bị xóa'
                    : 'Chưa được gán'}
                </strong>
              </div>
              <button
                type="button"
                className="is-primary"
                disabled={!effectiveRoomCode || selectedNode?.type !== 'DOOR'}
                onClick={() =>
                  selectedNode &&
                  mutation.mutate({
                    type: 'assign-room',
                    roomCode: effectiveRoomCode,
                    nodeId: selectedNode.id,
                  })
                }
              >
                <Save size={15} /> Gán vào node đang chọn
              </button>
              <button
                type="button"
                disabled={!effectiveRoomCode || !currentAssignment}
                onClick={() =>
                  mutation.mutate({
                    type: 'assign-room',
                    roomCode: effectiveRoomCode,
                    nodeId: null,
                  })
                }
              >
                <Unlink size={15} /> Bỏ gán phòng
              </button>
            </section>
          )}

          {editorStep === 'edges' && (
            <section className="sim-edge-list">
              <h3>
                <GitBranch size={17} /> Edge của {floor?.name}
              </h3>
              <p className="sim-map-muted">
                {floorNodes.length} node · {floorEdges.length} edge trong tầng
              </p>
              {floorEdges.map((edge) => (
                <div key={edge.id}>
                  <span>
                    {nodeById.get(edge.fromNodeId)?.name} ↔{' '}
                    {nodeById.get(edge.toNodeId)?.name}
                  </span>
                  <button
                    type="button"
                    title="Xóa edge"
                    onClick={() => {
                      if (window.confirm('Xóa edge này?')) {
                        mutation.mutate({
                          type: 'delete-edge',
                          edgeId: edge.id,
                        })
                      }
                    }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </section>
          )}
        </aside>
      </div>
    </div>
  )
}
