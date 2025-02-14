// organograma.js

// Variáveis globais
let root;       // Nó raiz da hierarquia
let svg, g;     // Referências ao SVG e ao grupo principal
let i = 0;      // Contador de IDs para nós
const width = 1200;
const height = 800;

// Seleciona o container do organograma
const container = d3.select("#organogramaContainer");

// Cria o SVG
svg = container.append("svg")
  .attr("width", width)
  .attr("height", height);

// Cria o grupo principal para os nós e links
g = svg.append("g")
  .attr("class", "org-group");

// Configura o comportamento de zoom e pan
const zoomBehavior = d3.zoom()
  .scaleExtent([0.5, 2])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });
svg.call(zoomBehavior);

// Define o layout da árvore com D3
const treeLayout = d3.tree().size([height, width - 200]);

// Carrega os dados do endpoint JSON
d3.json("/organograma/data/")
  .then(data => {
    // Cria a hierarquia dos dados
    root = d3.hierarchy(data);
    // Define posições iniciais para transição
    root.x0 = height / 2;
    root.y0 = 0;
    // Renderiza a árvore
    update(root);
  })
  .catch(err => {
    console.error("Erro ao carregar dados do organograma:", err);
  });

// Função principal de atualização do organograma
function update(source) {
  // Calcula o layout da árvore
  treeLayout(root);

  // Selecione os links e associe os dados
  const links = g.selectAll("line.link")
    .data(root.links(), d => d.target.id);

  // Links: entrada
  const linksEnter = links.enter().append("line")
    .attr("class", "link")
    .attr("stroke", "#999")
    .attr("x1", d => source.y0)
    .attr("y1", d => source.x0)
    .attr("x2", d => source.y0)
    .attr("y2", d => source.x0);

  // Transição dos links para suas novas posições
  linksEnter.merge(links)
    .transition()
    .duration(500)
    .attr("x1", d => d.source.y)
    .attr("y1", d => d.source.x)
    .attr("x2", d => d.target.y)
    .attr("y2", d => d.target.x);

  // Remove links que não são mais necessários
  links.exit()
    .transition()
    .duration(500)
    .attr("x1", d => source.y)
    .attr("y1", d => source.x)
    .attr("x2", d => source.y)
    .attr("y2", d => source.x)
    .remove();

  // Seleciona os nós e associa os dados
  const nodes = g.selectAll("g.node")
    .data(root.descendants(), d => d.id || (d.id = ++i));

  // Nós: entrada
  const nodeEnter = nodes.enter().append("g")
    .attr("class", "node")
    .attr("transform", d => `translate(${source.y0},${source.x0})`)
    .on("click", (event, d) => {
      // Ao clicar, alterna (expandir/colapsar) o nó e atualiza
      toggleChildren(d);
      update(d);
    });

  // Círculo representando o nó
  nodeEnter.append("circle")
    .attr("r", 1e-6)
    .attr("fill", d => d._children ? "#FFB74D" : "#4DB6AC")
    .attr("stroke", "#004D40")
    .attr("stroke-width", 2)
    .transition()
    .duration(500)
    .attr("r", 10);

  // Texto com o nome do nó
  nodeEnter.append("text")
    .attr("class", "label")
    .attr("dy", -15)
    .attr("text-anchor", "middle")
    .style("opacity", 0)
    .text(d => d.data.name)
    .transition()
    .duration(500)
    .style("opacity", 1);

  // Atualiza a posição dos nós já existentes
  const nodeUpdate = nodes.merge(nodeEnter)
    .transition()
    .duration(500)
    .attr("transform", d => `translate(${d.y},${d.x})`);

  // Salva a posição atual para as próximas transições
  root.descendants().forEach(d => {
    d.x0 = d.x;
    d.y0 = d.y;
  });

  // Remove nós que não serão mais exibidos
  nodes.exit()
    .transition()
    .duration(500)
    .attr("transform", d => `translate(${source.y},${source.x})`)
    .remove();
}

// Função para alternar (expandir/colapsar) um nó ao clicar
function toggleChildren(d) {
  if (d.children) {
    // Colapsa: move children para _children
    d._children = d.children;
    d.children = null;
  } else {
    // Expande: move _children para children
    d.children = d._children;
    d._children = null;
  }
}

// Função para expandir toda a árvore
function expandAll(d) {
  if (d._children) {
    d.children = d._children;
    d._children = null;
  }
  if (d.children) {
    d.children.forEach(expandAll);
  }
}

// Função para colapsar nós abaixo de um nível específico (maxDepth = 2)
// Exibe: raiz (depth 0), filhos (depth 1) e netos (depth 2)
function collapseAtLevel(d, maxDepth) {
  if (d.depth >= maxDepth && d.children) {
    d._children = d.children;
    d.children = null;
  }
  if (d.children) {
    d.children.forEach(child => collapseAtLevel(child, maxDepth));
  }
  if (d._children) {
    d._children.forEach(child => collapseAtLevel(child, maxDepth));
  }
}

// Botões de controle

// Botão para expandir todos os nós
document.getElementById("expandAllBtn").addEventListener("click", () => {
  if (!root) return;
  expandAll(root);
  update(root);
});

// Botão para colapsar a árvore mantendo apenas 2 níveis
document.getElementById("collapseBtn").addEventListener("click", () => {
  if (!root) return;
  // Primeiro, garante que toda a árvore esteja expandida
  expandAll(root);
  // Em seguida, colapsa nós com depth maior ou igual a 2 (netos e abaixo)
  if (root.children) {
    root.children.forEach(child => collapseAtLevel(child, 2));
  }
  update(root);
});
