// organograma.js

// Variáveis globais
let root // Nó raiz da hierarquia
let svg, g // Referências ao SVG e ao grupo principal
let i = 0 // Contador de IDs para nós
const width = 1200
const height = 800
let tooltip // Tooltip para informações adicionais

// Paleta de cores minimalista
const colors = {
  node: {
    default: '#f8fafd',
    expanded: '#e9f0f9',
    hover: '#e9f0f9',
    stroke: '#d1d9e6'
  },
  text: '#333333',
  link: '#a4c5f4'
}

// Seleciona o container do organograma
const container = d3.select('#organogramaContainer')

// Adiciona o título e botões diretamente no HTML
container.node().innerHTML += `
  <div class="org-title">Organograma Institucional</div>
  <div class="org-buttons-bar">
    <button id="expandAllBtn" class="control-btn"><i class="fas fa-expand-arrows-alt"></i> Expandir Todos</button>
    <button id="collapseBtn" class="control-btn"><i class="fas fa-compress-arrows-alt"></i> Colapsar</button>
    <button id="resetBtn" class="control-btn"><i class="fas fa-sync"></i> Resetar Zoom</button>
  </div>
`

// Cria o tooltip
tooltip = container.append('div').attr('class', 'tooltip').style('opacity', 0)

// Cria o SVG
svg = container
  .append('svg')
  .attr('width', '100%')
  .attr('height', '100%')
  .attr('viewBox', `0 0 ${width} ${height}`)
  .attr('preserveAspectRatio', 'xMidYMid meet')

// Cria o grupo principal para os nós e links
g = svg
  .append('g')
  .attr('class', 'org-group')
  .attr('transform', `translate(${width / 2}, 80)`)

// Configura o comportamento de zoom e pan
const zoomBehavior = d3
  .zoom()
  .scaleExtent([0.5, 2])
  .on('zoom', event => {
    g.attr('transform', event.transform)
  })
svg.call(zoomBehavior)

// Define o layout da árvore com D3
const treeLayout = d3
  .tree()
  .nodeSize([80, 200])
  .separation((a, b) => (a.parent === b.parent ? 1.2 : 1.5))

// Carrega os dados do JSON local
d3.json('/static/data/organograma.json')
  .then(data => {
    // Cria a hierarquia dos dados
    root = d3.hierarchy(data[0])

    // Define posições iniciais para transição
    root.x0 = 0
    root.y0 = 0

    // Colapsa todos os nós exceto o primeiro nível
    if (root.children) {
      // Aplica a função collapseAtLevel com nível 1 para manter apenas o primeiro nível expandido
      root.children.forEach(child => collapseAtLevel(child, 0))
    }

    // Renderiza a árvore
    update(root)

    // Centraliza inicialmente
    const initialTransform = d3.zoomIdentity
      .translate(width / 2, height / 6)
      .scale(0.85)
    svg.call(zoomBehavior.transform, initialTransform)
  })
  .catch(err => {
    console.error('Erro ao carregar dados do organograma:', err)
    // Exibe mensagem de erro no container
    container
      .append('div')
      .attr('class', 'alert alert-danger')
      .html(
        "<i class='fas fa-exclamation-circle me-2'></i>Não foi possível carregar os dados do organograma."
      )
  })

// Função principal de atualização do organograma
function update(source) {
  // Calcula o layout da árvore
  const duration = 500 // duração da transição em ms

  // Aplica o layout da árvore
  treeLayout(root)

  // Normaliza para layout horizontal (y = horizontal, x = vertical)
  root.descendants().forEach(d => {
    // Troca x e y para layout horizontal
    const temp = d.x
    d.x = d.y
    d.y = temp
  })

  // Selecione todos os nós
  const nodes = g
    .selectAll('g.node')
    .data(root.descendants(), d => d.id || (d.id = ++i))

  // ENTRADA: Cria novos nós
  const nodeEnter = nodes
    .enter()
    .append('g')
    .attr(
      'class',
      d =>
        `node ${d.children || d._children ? 'node--internal' : 'node--leaf'} ${
          d._children ? 'collapsed' : ''
        }`
    )
    .attr('transform', d => `translate(${source.x0},${source.y0})`)
    .style('opacity', 0)
    .on('click', (event, d) => {
      event.stopPropagation()
      toggleChildren(d)
      update(d)
    })
    .on('mouseover', (event, d) => {
      // Mostra tooltip com secretaria
      tooltip.transition().duration(200).style('opacity', 1)

      tooltip
        .html(
          `
        <h4>${d.data.nome}</h4>
        <p>${d.data.cargo || 'Cargo não especificado'}</p>
        <div class="tooltip-field">
          <span class="tooltip-label">Secretaria:</span>
          <span class="tooltip-value">${
            d.data.secretaria || 'Não especificada'
          }</span>
        </div>
      `
        )
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY - 28 + 'px')

      // Destaca o nó
      d3.select(event.currentTarget)
        .select('circle')
        .transition()
        .duration(200)
        .attr('r', 12)
    })
    .on('mouseout', (event, d) => {
      // Esconde tooltip
      tooltip.transition().duration(500).style('opacity', 0)

      // Remove destaque
      d3.select(event.currentTarget)
        .select('circle')
        .transition()
        .duration(200)
        .attr('r', 8)
    })

  // Adiciona círculos aos novos nós
  nodeEnter
    .append('circle')
    .attr('r', 0)
    .attr('fill', d =>
      d._children ? colors.node.expanded : colors.node.default
    )
    .attr('stroke', colors.node.stroke)
    .attr('stroke-width', 1.5)

  // Adiciona texto para o nome
  nodeEnter
    .append('text')
    .attr('class', 'label-nome')
    .attr('dy', -15)
    .attr('x', 0)
    .attr('text-anchor', 'middle')
    .text(d => d.data.nome)
    .style('fill-opacity', 0)

  // Adiciona texto para o cargo
  nodeEnter
    .append('text')
    .attr('class', 'label-cargo')
    .attr('dy', 0)
    .attr('x', 0)
    .attr('text-anchor', 'middle')
    .text(d => d.data.cargo)
    .style('fill-opacity', 0)
    .style('font-size', '10px')
    .style('fill', '#666')

  // ATUALIZAÇÃO: Transição para novas posições
  const nodeUpdate = nodeEnter
    .merge(nodes)
    .transition()
    .duration(duration)
    .attr('transform', d => `translate(${d.x},${d.y})`)
    .style('opacity', 1)

  // Atualiza aparência dos nós
  nodeUpdate
    .select('circle')
    .attr('r', 8)
    .attr('fill', d =>
      d._children ? colors.node.expanded : colors.node.default
    )

  // Atualiza texto
  nodeUpdate.selectAll('text').style('fill-opacity', 1)

  // SAÍDA: Remove nós que não são mais necessários
  const nodeExit = nodes
    .exit()
    .transition()
    .duration(duration)
    .attr('transform', d => `translate(${source.x},${source.y})`)
    .style('opacity', 0)
    .remove()

  // Reduz tamanho dos círculos na saída
  nodeExit.select('circle').attr('r', 0)

  // Desvanece texto na saída
  nodeExit.selectAll('text').style('fill-opacity', 0)

  // Atualiza os links (conexões entre nós)
  const links = g.selectAll('path.link').data(root.links(), d => d.target.id)

  // Função para gerar curvas suaves para os links
  const diagonal = d3
    .linkHorizontal()
    .x(d => d.x)
    .y(d => d.y)

  // ENTRADA: Adiciona novos links
  const linkEnter = links
    .enter()
    .append('path')
    .attr('class', 'link')
    .attr('d', d => {
      const o = { x: source.x0, y: source.y0 }
      return diagonal({ source: o, target: o })
    })
    .attr('fill', 'none')
    .attr('stroke', colors.link)
    .attr('stroke-width', 2)
    .attr('stroke-opacity', 0.7)

  // ATUALIZAÇÃO: Transição para novas posições
  linkEnter.merge(links).transition().duration(duration).attr('d', diagonal)

  // SAÍDA: Remove links que não são mais necessários
  links
    .exit()
    .transition()
    .duration(duration)
    .attr('d', d => {
      const o = { x: source.x, y: source.y }
      return diagonal({ source: o, target: o })
    })
    .remove()

  // Armazena as posições atuais para a próxima transição
  root.descendants().forEach(d => {
    d.x0 = d.x
    d.y0 = d.y
  })
}

// Função para alternar a exibição dos filhos
function toggleChildren(d) {
  if (d.children) {
    d._children = d.children
    d.children = null
  } else if (d._children) {
    d.children = d._children
    d._children = null
  }
}

// Função para expandir todos os nós
function expandAll(d) {
  if (d._children) {
    d.children = d._children
    d._children = null
  }
  if (d.children) d.children.forEach(expandAll)
}

// Função para colapsar nós a partir de um certo nível
function collapseAtLevel(d, level = 0) {
  // Se o nó tem filhos e não é o nó raiz (ou está abaixo do nível especificado)
  if (d.children && d.depth > level) {
    d._children = d.children
    d.children = null
  }
  // Se o nó tem filhos e está no nível especificado ou acima, colapsa seus filhos
  else if (d.children) {
    d.children.forEach(child => collapseAtLevel(child, level))
  }
}

// Função para colapsar todos os nós, mantendo apenas o nó raiz expandido
function collapseAll(d) {
  if (d.children) {
    // Para cada filho, primeiro colapsa todos os seus descendentes
    d.children.forEach(collapseAll)

    // Depois colapsa o próprio filho (exceto se for o nó raiz)
    if (d.depth > 0) {
      d._children = d.children
      d.children = null
    }
  }
}

// Adiciona eventos aos botões de controle
document.getElementById('expandAllBtn').addEventListener('click', () => {
  expandAll(root)
  update(root)
})

document.getElementById('collapseBtn').addEventListener('click', () => {
  // Colapsa todos os nós, exceto o nó raiz
  collapseAll(root)
  update(root)
})

document.getElementById('resetBtn').addEventListener('click', () => {
  const initialTransform = d3.zoomIdentity
    .translate(width / 2, height / 6)
    .scale(0.85)
  svg.call(zoomBehavior.transform, initialTransform)
})

// Função para ajustar o tamanho do SVG quando a janela é redimensionada
function resizeOrganograma() {
  const containerWidth = container.node().getBoundingClientRect().width
  const containerHeight = container.node().getBoundingClientRect().height

  svg.attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
}

// Adiciona evento de redimensionamento
window.addEventListener('resize', resizeOrganograma)

// Chama a função de redimensionamento quando a página carrega
window.addEventListener('load', resizeOrganograma)
