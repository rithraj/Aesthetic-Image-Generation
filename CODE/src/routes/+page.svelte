<!-- src/Scatterplot.svelte -->
<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  import searchData from '../data/data-reduced.json'
  import FlexSearch from 'flexsearch/dist/flexsearch.es5.js'
  
  // Constants
  const fixedFloatLength = 4;
  const scaleFactorX = 50;
  const scaleFactorY = 30;

  // Initialize Variables
  var index = new FlexSearch.FlexSearch.Index()

  let model;
  let data = null;
  let width;
  let height;
  let svg, g;

  let xValues, yValues;
  let minX, maxX, minY, maxY;
  let centerX, centerY;

  let currHoveredData;

  let collapsedSearch = false;

  let filterOptions = [
    { label: 'Top 500', value: 500 },
    { label: 'All', value: 0 },
    { label: 'Top 2500', value: 2500 },
    { label: 'Top 5000', value: 5000 },
    { label: 'Above 60', value: 60 },
    { label: 'Below 15', value: 15}
  ];

  // Selected filter value
  let selectedFilter = filterOptions[0].value;


  function formatData(data) {
    const result = Object.entries(data).map(([key, values], idx) => {
      index.add(key, values["prompt"]);
      return {
        x: values["x"],
        y: values["y"],
        prompt: values["prompt"],
        iaa_score: values["iaa_score"],
        id: values["id"],
        part_id: values["part_id"],
      }
    })
    return result
  }

  function initializeValues() {
    data = formatData(searchData);
    xValues = data.map(d => d.x);
    yValues = data.map(d => d.y);
    minX = Math.min(...xValues);
    maxX = Math.max(...xValues);
    minY = Math.min(...yValues);
    maxY = Math.max(...yValues);
    centerX = (minX + maxX) / 2;
    centerY = (minY + maxY) / 2;
  }

  // Create a zoom behavior
  const zoom = d3.zoom()
    .scaleExtent([0.05, 8]) // Set the min and max zoom levels
    .on('zoom', zoomed);

  function zoomed(event) {
    g.attr('transform', event.transform);
  }

  // Function to render the scatterplot
  function renderScatterplot() {
    // Create the SVG container
    svg = d3.select('#scatterplot')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .call(zoom);

    g = svg.append('g');

    // static sized circle to appear on hover
    svg.append('circle')
      .attr('id', 'hover-circle')
      .attr('r', 10)
      .attr('fill', 'black')
      .style('display', 'none')
      .raise()
      .on('mouseout', onMouseOut);
  }

  function updateSearchIndex(data) {
    index = new FlexSearch.FlexSearch.Index();

    for (const item of data) {
      index.add(item.id, item.prompt)
    }
  }

  function updateData() {
    let filteredData;
    // Three cases based on values:
    // 1) take scores above threshold
    // 2) take scores below threshold
    // 3) take top k sorted points by score
    if (selectedFilter === 60 || selectedFilter === 0) {
      filteredData = data.filter(d => d.iaa_score > selectedFilter);
    } else if (selectedFilter === 15) {
      filteredData = data.filter(d => d.iaa_score < selectedFilter);
    } else {
      filteredData = data
        .slice()
        .sort((a, b) => b.iaa_score - a.iaa_score)
        .slice(0, selectedFilter);
    }

    // update index to only search filtered points
    updateSearchIndex(filteredData)
    searchTermChanged();

    // Create circles for each data point centered on the page
    g.selectAll('circle')
      .data(filteredData)
      .join('circle')
      .attr('cx', d => d.x*scaleFactorX - centerX + width / 2)
      .attr('cy', d => d.y*scaleFactorY - centerY + height / 2)
      .attr('opacity', 0.7)
      .attr('r', 1) // Radius of the circles
      .attr('fill', 'steelblue')
      .on('mouseover', onMouseOver)
  }

  // called by each data point
  function onMouseOver(event, d) {
    currHoveredData = d;

    // move hover circle over data point
    const ct = d3.zoomTransform(svg.node())
    d3.select('#hover-circle')
      .attr('cx', (d.x*scaleFactorX - centerX + width / 2)* ct.k + ct.x )
      .attr('cy', (d.y*scaleFactorY - centerY + height / 2)*  ct.k + ct.y)
      .attr('r', ct.k)
      .style('display', 'block')
    
      if (d.publicUrl === undefined) {
      d.timeoutId = setTimeout(() => showTooltipText(event, d), 0);
      d.timeoutId = setTimeout(() => showTooltip(event, d), 800);
    } else {
      showTooltip(event, d);
    }
  }

  // called by hover circle
  // since moved in front of data point, mouseOut acts on this circle
  function onMouseOut(event, d) {
    // hide hover circle
    d3.select("#hover-circle")
      .style('display', 'none')

    clearTimeout(currHoveredData.timeoutId);
    currHoveredData.timeoutId = 0;
    hideTooltip();
  }

  // Function to show the tooltip
  function showTooltip(event, d) {
    d.publicUrl = `https://storage.googleapis.com/diffusiondb-images/${d.part_id}/${d.id}`
    var wdth = Math.max((d.prompt).length, 200)
    d3.select('#tooltip')
      .style('left', `${event.clientX}px`)
      .style('top', `${event.clientY - 30}px`)
      .html(`<p style="margin-top:0;">Prompt: ${d.prompt}</p>
              <p>Image Aesthetic Score: ${d.iaa_score}</p>
              <div width="100%"" style="display:flex; justify-content:center">
                <img src=${d.publicUrl} width=${wdth} height=${wdth}></img>
              </div>`)
      .style('opacity', 1)
  }
  function showTooltipText(event, d) {
    var wdth = Math.max((d.prompt).length, 200)
    d3.select('#tooltip')
      .style('left', `${event.clientX}px`)
      .style('top', `${event.clientY - 30}px`)
      .html(`<p style="margin-top:0;">Prompt: ${d.prompt}</p>
              <p>Image Aesthetic Score: ${d.iaa_score}</p>
              <div width="100%"" style="display:flex; justify-content:center">
              </div>`)
      .style('opacity', 1)
  }

  // Function to hide the tooltip
  function hideTooltip() {
    d3.select('#tooltip')
      .style('opacity', 0);
  }

  onMount(() => {
    if (!data) {
      initializeValues()
    }

    // loadModel()

    if (typeof window !== 'undefined') {
      width = window.innerWidth;
      height = window.innerHeight;
      renderScatterplot();
      updateData();
    } else {
      console.error('Window object is not defined.');
    }
  });

  let searchTerm = "";
  let searchResults = [];
  let searchResultsCount = 0;
  var searchLimit = 20;

  function searchTermChanged() {
    searchLimit = 20;
    if (searchTerm.length < 2) {
      return;
    }
    const res = index.search(searchTerm)
    searchResultsCount = res.length
    searchResults = res
  }

  let selectedSort = 'Descending';
	
	function onSortChange(event) {
		selectedSort = event.currentTarget.value;
	}

  function increaseLimit() {
    searchLimit = 100000;
  }

  function clearSearch() {
    searchTerm = '';
    searchResults = [];
    searchResultsCount = 0;
    collapsedSearch = false;
  }

  let prevSelected = null;

  function zoomToPoint(result) {
    if (prevSelected) {
      g.selectAll('circle')
      .filter(d => d.id === prevSelected)
        .attr('fill', 'steelblue')
        .attr('radius', 1)
        .attr('opacity', 0.7);
    }

    const dataX = result.x*scaleFactorX - centerX + width / 2
    const dataY = result.y*scaleFactorY - centerY + height / 2

    // Zoom and center on data point
    // zoom.scaleTo(svg, 8);
    // zoom.translateTo(svg, dataX, dataY);  
    svg.transition()
    .duration(750) // Set the duration of the transition in milliseconds
    .call(zoom.scaleTo, 8)
    .call(zoom.translateTo, dataX, dataY);
    // Color the selected point red
    g.selectAll('circle')
    .filter(d => d.id === result.id)
    .attr('fill', 'red')
    .attr('opacity', 1)
    .attr('r', 1)
    .raise();

    const d = data.filter(d => d.id === result.id)[0]
    showTooltip({clientX: width/2, clientY: height/2}, d)
    
    prevSelected = result.id;
  }

  function toggleCollapse() {
    collapsedSearch = !collapsedSearch;
  }
</script>
  
<style>
  p {
    margin: 0;
  }
  .container {
    position: fixed;
    font-family: 'Open Sans', sans-serif;
  }

  #tooltip {
    position: absolute;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 5px;
    border-radius: 5px;
    pointer-events: none;
    opacity: 0;
    max-width: 300px;
  }

  #scatterplot {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
  }

  #filter {
    display: block;
    padding-bottom: 10px;
  }

  #search-results-container {
    display: flex;
    flex-direction: column;
    width: 450px;
    border: 1px solid black;
    margin-top: 10px;
    background-color: white;
    overflow: auto;
    max-height:70vh;
    position: relative;
  }

  .action-buttons {
    display: flex;
    position: absolute;
    top: 5px;
    right: 5px;
  }

  .clear-button {
    position: relative;
    margin-right: 5px;
    width: auto;
  }

  .collapse-button, .clear-button {
    cursor: pointer;
  }

  .collapsedSearch {
    height: 30px;
    overflow: hidden;
  }

  .search-results {
    padding: 10px;
  }

  .searchItem {
    width: 100%;
    text-align: left;
  }

  .searchItem p {
    overflow: hidden;
    white-space: normal;
    margin: 0;
  }

  .iaa-score {
    font-weight: bold;
    margin-top: 4px;
  }

</style>

<div class="container">
  <h1 id="title">DiffusionDB Image Aesthetics</h1>

  <div id="filter">
    <label for="filterSelect">Select filter:</label>
    <select id="filterSelect" bind:value={selectedFilter} on:change={updateData}>
      {#each filterOptions as option}
        <option value={option.value}>{option.label}</option>
      {/each}
    </select>
  </div>

  <input id="searchInput" type="search" placeholder="Search..." bind:value={searchTerm} on:input={searchTermChanged}/>

  <label>
	  <input checked={selectedSort==='Descending'} on:change={onSortChange} type="radio" name="sort" value="Descending" /> Descending
  </label>
  <label>
	  <input checked={selectedSort==='Ascending'} on:change={onSortChange} type="radio" name="sort" value="Ascending" /> Ascending
  </label>

  {#if searchResults.length > 0}
    <div id="search-results-container" class="{collapsedSearch ? 'collapsedSearch' : ''}">
      <div class="action-buttons">
        <button class="clear-button" on:click={clearSearch}>Clear</button>
        <button class="collapse-button" on:click={toggleCollapse}>{collapsedSearch ? 'Show' : 'Collapse'}</button>
      </div>
  
      <div class="search-results">
        <p>{searchResultsCount} results.</p>
      </div>
    
      {#each searchResults.slice(0,searchLimit).map(i => searchData[i]).sort((a,b) => (selectedSort === "Descending" ?  b.iaa_score - a.iaa_score : a.iaa_score - b.iaa_score)) as result, i}
        <button on:mouseenter={() => zoomToPoint(result)} on:mouseleave={hideTooltip} class="searchItem">
          <p>{result.prompt.slice(0, 125)}{result.prompt.length > 125 ? '...' : ''}</p>
          <p class="iaa-score">IAA: {result.iaa_score.toFixed(fixedFloatLength)}</p>
        </button>
      {/each}
      {#if searchLimit == 20}
      <button id="load-more-btn" on:click={increaseLimit}>
        Load more
      </button>
      {/if}
    </div>

  {/if}

  <div id="scatterplot">
  </div>
  <div id="tooltip"></div>
</div>
