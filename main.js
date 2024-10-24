function fetchData(){
    fetch('./realproducts.json')
    .then((response) => response.json())
    .then((json) => createTable(json));
}

function createTable(json){
    const table      = document.createElement("table");
    const headerRow  = document.createElement("tr");
    const detailsRow = document.createElement("tr");
    const curPeriod  = json[0]["current_period_time"]
    const refPeriod  = json[0]["reference_period_time"]  
    table.setAttribute("id", "kpi");
    headerRow.innerHTML = "<th colspan='2'>Product</th> <th colspan='1'>Stuks per dag</th><th colspan='1'>Aantal stuks</th><th colspan='1'>Orders</th>";
    table.appendChild(headerRow);
    detailsRow.innerHTML = "<th id='details' colspan='2'></th> <th id='details'><p id='nu' abbr title="+curPeriod+">Nu</p> <p id='voor' abbr title="+refPeriod+">Voor</p></th><th id='details'><p id='nu' abbr title="+curPeriod+">Nu</p> <p id='voor' abbr title="+refPeriod+">Voor</p></th><th id='details'><p id='nu' abbr title="+curPeriod+">Nu</p> <p id='voor' abbr title="+refPeriod+">Voor</p></th>";
    table.appendChild(detailsRow);
    for (let i = 0; i < json.length; i++) {
        const element = json[i]
        if(i >= 25) break;
        table.appendChild(createDataRow(element, i));
    }
    document.body.append(table);
};

function createDataRow(e, i){
        const dataRow                   = document.createElement("tr");
        const quantityPerDayText        = formatNumberOrLessThanOne(e["current_display_stats"]["quantityPerDay"]).toString().padStart(5, "_")
        const precentQuantityPerDayText = e["current_display_stats"]["quantityPerDayChange"].toString().padStart(5, "_")

        const totalQuantityText = Math.round(e["current_display_stats"]["totalQuantity"]*5.5).toString().padStart(5, "_")
       //const precentTotalQuantityText  = e["current_display_stats"]["totalQuantityChange"].toString().padStart(4, "_")
        
        const totalOrdersText        = Math.round(e["current_display_stats"]["totalOrders"]*5.5).toString().padStart(5, "_")
        const precentTotalOrdersText = e["current_display_stats"]["totalOrdersChange"].toString().padStart(5, "_")

        const refQuantityPerDayText = formatNumberOrLessThanOne(e["reference_display_stats"]["quantityPerDay"]).toString().padStart(5, "_")
        const refTotalQuantityText  = e["reference_display_stats"]["totalQuantity"].toString().padStart(5, "_")
        const refTotalOrdersText    = e["reference_display_stats"]["totalOrders"].toString().padStart(5, "_")
        const elClass = (i % 2) ? "newColor" : "";

        dataRow.innerHTML = (
          "<td class="+elClass+"><p  id='rank'>"+(i+1)+"</p></td>"
        + "<td class="+elClass+"><p  id='name'>"+e["name"]+"</p></td>"

        + "<td class="+elClass+"><p >"+quantityPerDayText.replaceAll('_', '&nbsp;')+"</p>"
        + "<p>"+generateChangeIcon(e["current_display_stats"]["quantityPerDayChange"])+precentQuantityPerDayText.replaceAll('_', '&nbsp;')+"%</p>"
        + "<p>"+refQuantityPerDayText.replaceAll('_', '&nbsp;')+"</p></td>" 

        + "<td class="+elClass+"><p>"+totalQuantityText.replaceAll('_', '&nbsp;')+"</p>" 
        + "<p>"+generateChangeIcon(e["current_display_stats"]["quantityPerDayChange"])+precentQuantityPerDayText.replaceAll('_', '&nbsp;')+"%</p>" 
        + "<p>"+refTotalQuantityText.replaceAll('_', '&nbsp;')+"</p></td>" 

        + "<td class="+elClass+"><p>"+totalOrdersText.replaceAll('_', '&nbsp;')+"</p>"
        + "<p>"+generateChangeIcon(e["current_display_stats"]["totalOrdersChange"]*5.5)+precentTotalOrdersText.replaceAll('_', '&nbsp;')+"%</p>" 
        + "<p>"+refTotalOrdersText.replaceAll('_', '&nbsp;')+"</p></td>"
        );     
        return dataRow;
}

function formatNumberOrLessThanOne(number){
    if(Math.round(number) < 1)
        return "<1"
    else
        return Math.round(number)
}

function generateChangeIcon(currentChange){
    if(currentChange > 0)
        return '<i id="positive" class="fa fa-caret-up"></i>'
    else if(currentChange < 0)
        return '<i id="negative" class="fa fa-caret-down"></i>'
    else
        return '<i class="fa fa-minus"></i>'
}

var form = document.getElementById("myForm");
function handleForm() {
    fetchData();
    setInterval(function(){
        try {
            document.getElementById("kpi").remove();
        } catch (error) {
            console.log(error);
        }
        fetchData();

    }, 5000*60)
    
};
addEventListener('DOMContentLoaded', handleForm);
