import { expect, test } from '@playwright/test'

const apiUrl =
  process.env.PLAYWRIGHT_API_URL ?? 'http://127.0.0.1:8011/api/v1'

interface GraphPayload {
  nodes: Array<{
    id: string
    floor_id: string
    name: string
    type: string
    connector_code: string | null
  }>
  edges: Array<{
    from_node_id: string
    to_node_id: string
    is_inter_floor: boolean
  }>
}

test.describe('Cấu hình sơ đồ chỉ đường', () => {
  test.describe.configure({ mode: 'serial' })

  test('giữ liên kết sơ đồ chỉ đường trong trang danh mục chỉ định', async ({
    page,
  }) => {
    await page.goto('/demo/hospital-data')

    const mapLink = page.getByRole('link', { name: 'Sơ đồ chỉ đường' })
    await expect(mapLink).toBeVisible()
    await mapLink.click()

    await expect(page).toHaveURL(/\/demo\/simulator\?tab=map$/)
    await expect(
      page.getByRole('heading', { name: 'Cấu hình sơ đồ chỉ đường' }),
    ).toBeVisible()
  })

  test('lưu node vào cơ sở dữ liệu và vẫn hiển thị sau khi tải lại', async ({
    page,
    request,
  }) => {
    let nodeId: string | undefined
    let nodeName: string | undefined

    try {
      const beforeResponse = await request.get(
        `${apiUrl}/indoor-navigation/graph`,
      )
      const beforeGraph = (await beforeResponse.json()) as GraphPayload
      const nodeIdsBefore = new Set(beforeGraph.nodes.map((node) => node.id))

      await page.goto('/demo/simulator?tab=map')
      await expect(
        page.getByRole('heading', {
          name: 'Chỉnh mạng đường đi của bệnh viện',
        }),
      ).toBeVisible()

      await page
        .locator('.sim-node-palette button')
        .filter({ hasText: 'Hành lang' })
        .click()
      await page.locator('.sim-map-canvas').click({ position: { x: 180, y: 180 } })

      await expect(
        page.getByText('Đã tạo node định vị và lưu vào cơ sở dữ liệu.'),
      ).toBeVisible()

      const graphResponse = await request.get(
        `${apiUrl}/indoor-navigation/graph`,
      )
      expect(graphResponse.ok()).toBeTruthy()
      const graph = (await graphResponse.json()) as GraphPayload
      const createdNode = graph.nodes.find((node) => !nodeIdsBefore.has(node.id))
      nodeId = createdNode?.id
      nodeName = createdNode?.name
      expect(nodeId).toBeTruthy()
      expect(nodeName).toBeTruthy()

      await page.reload()
      await expect(
        page.locator(`.sim-route-node[title^="${nodeName}"]`),
      ).toHaveCount(1)
    } finally {
      if (nodeId) {
        const deleteResponse = await request.delete(
          `${apiUrl}/simulation/indoor-navigation/nodes/${encodeURIComponent(nodeId)}`,
        )
        expect(deleteResponse.ok()).toBeTruthy()
      }
    }
  })

  test('tự cấp cùng trục và nối cầu thang ở hai tầng liền kề', async ({
    page,
    request,
  }) => {
    const createdNodeIds: string[] = []

    try {
      const beforeResponse = await request.get(
        `${apiUrl}/indoor-navigation/graph`,
      )
      const beforeGraph = (await beforeResponse.json()) as GraphPayload
      const nodeIdsBefore = new Set(beforeGraph.nodes.map((node) => node.id))

      await page.goto('/demo/simulator?tab=map')
      await page
        .locator('.sim-node-palette button')
        .filter({ hasText: 'Cầu thang' })
        .click()
      const firstCreateResponse = page.waitForResponse(
        (response) =>
          response.url().includes('/simulation/indoor-navigation/nodes') &&
          response.request().method() === 'POST',
      )
      await page.locator('.sim-map-canvas').click({ position: { x: 220, y: 190 } })
      expect((await firstCreateResponse).ok()).toBeTruthy()
      await expect(
        page.getByText('Đã tạo điểm và tự đồng bộ trục liên tầng A/B/C.'),
      ).toBeVisible()

      await page.getByLabel('Tầng đang chỉnh').selectOption('hospital-floor-2')
      const secondCreateResponse = page.waitForResponse(
        (response) =>
          response.url().includes('/simulation/indoor-navigation/nodes') &&
          response.request().method() === 'POST',
      )
      await page.locator('.sim-map-canvas').click({ position: { x: 230, y: 200 } })
      expect((await secondCreateResponse).ok()).toBeTruthy()
      await expect(
        page.getByText('Đã tạo điểm và tự đồng bộ trục liên tầng A/B/C.'),
      ).toBeVisible()

      const afterResponse = await request.get(
        `${apiUrl}/indoor-navigation/graph`,
      )
      const afterGraph = (await afterResponse.json()) as GraphPayload
      const createdNodes = afterGraph.nodes.filter(
        (node) => !nodeIdsBefore.has(node.id),
      )
      createdNodeIds.push(...createdNodes.map((node) => node.id))

      expect(createdNodes).toHaveLength(2)
      expect(createdNodes[0].connector_code).toBeTruthy()
      expect(createdNodes[0].connector_code).toBe(createdNodes[1].connector_code)
      expect(
        afterGraph.edges.some(
          (edge) =>
            edge.is_inter_floor &&
            createdNodeIds.includes(edge.from_node_id) &&
            createdNodeIds.includes(edge.to_node_id),
        ),
      ).toBeTruthy()
    } finally {
      for (const nodeId of createdNodeIds) {
        const deleteResponse = await request.delete(
          `${apiUrl}/simulation/indoor-navigation/nodes/${encodeURIComponent(nodeId)}`,
        )
        expect(deleteResponse.ok()).toBeTruthy()
      }
    }
  })
})
