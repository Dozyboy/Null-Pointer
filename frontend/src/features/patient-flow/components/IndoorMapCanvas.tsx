import { Crosshair, Minus, Plus, RotateCcw } from 'lucide-react'
import { TransformComponent, TransformWrapper } from 'react-zoom-pan-pinch'
import type {
  IndoorFloor,
  IndoorRouteNode,
} from '../model/indoor-navigation.types'
import './indoor-navigation.css'

interface IndoorMapCanvasProps {
  floor: IndoorFloor
  currentNode?: IndoorRouteNode
  route: IndoorRouteNode[]
  destinationNode?: IndoorRouteNode
  compact?: boolean
}
export function IndoorMapCanvas({
  floor,
  currentNode,
  route,
  destinationNode,
  compact = false,
}: IndoorMapCanvasProps) {
  const routePoints = route
    .map(
      (node) =>
        `${(node.xPercent * floor.mapWidth) / 100},${
          (node.yPercent * floor.mapHeight) / 100
        }`,
    )
    .join(' ')

  return (
    <div
      className={`indoor-map-shell ${compact ? 'is-compact' : ''}`}
      data-testid="indoor-map"
    >
      <TransformWrapper
        initialScale={1}
        minScale={0.8}
        maxScale={4}
        centerOnInit
        wheel={{ step: 0.12 }}
        doubleClick={{ mode: 'zoomIn' }}
      >
        {({ zoomIn, zoomOut, resetTransform, centerView }) => (
          <>
            <div className="indoor-map-tools" aria-label="Điều khiển bản đồ">
              <button type="button" onClick={() => zoomIn()} aria-label="Phóng to">
                <Plus />
              </button>
              <button type="button" onClick={() => zoomOut()} aria-label="Thu nhỏ">
                <Minus />
              </button>
              <button
                type="button"
                onClick={() => resetTransform()}
                aria-label="Đặt lại bản đồ"
              >
                <RotateCcw />
              </button>
              <button
                type="button"
                onClick={() => centerView()}
                aria-label="Căn giữa bản đồ"
              >
                <Crosshair />
              </button>
            </div>
            <TransformComponent
              wrapperClass="indoor-transform-wrapper"
              contentClass="indoor-transform-content"
            >
              <div
                className="indoor-map-stage"
                style={{ aspectRatio: `${floor.mapWidth}/${floor.mapHeight}` }}
              >
                <img
                  className="indoor-floor-map"
                  src={floor.mapImageUrl}
                  alt={`Sơ đồ ${floor.name}`}
                />
                {route.length > 0 && (
                  <svg
                    className="indoor-route-overlay"
                    viewBox={`0 0 ${floor.mapWidth} ${floor.mapHeight}`}
                    preserveAspectRatio="none"
                    aria-label="Đường đi được đề xuất"
                  >
                    {route.length > 1 && (
                      <>
                        <polyline
                          className="indoor-route-border"
                          points={routePoints}
                        />
                        <polyline
                          className="indoor-route-line"
                          points={routePoints}
                        />
                      </>
                    )}
                    {destinationNode?.floorId === floor.id && (
                      <>
                        <circle
                          className="indoor-destination-pulse"
                          cx={(destinationNode.xPercent * floor.mapWidth) / 100}
                          cy={(destinationNode.yPercent * floor.mapHeight) / 100}
                          r="22"
                        />
                        <circle
                          className="indoor-route-destination"
                          cx={(destinationNode.xPercent * floor.mapWidth) / 100}
                          cy={(destinationNode.yPercent * floor.mapHeight) / 100}
                          r="13"
                        />
                      </>
                    )}
                  </svg>
                )}
                {currentNode?.floorId === floor.id && (
                  <div
                    className="indoor-user-marker"
                    style={{
                      left: `${currentNode.xPercent}%`,
                      top: `${currentNode.yPercent}%`,
                    }}
                    aria-label={`Vị trí bắt đầu: ${currentNode.name}`}
                  >
                    <div className="indoor-accuracy-circle" />
                    <div className="indoor-blue-dot" />
                  </div>
                )}
              </div>
            </TransformComponent>
          </>
        )}
      </TransformWrapper>
    </div>
  )
}
