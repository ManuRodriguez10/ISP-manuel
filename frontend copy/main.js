window.addEventListener("DOMContentLoaded", (event) => {
    getVisitCount();
})

const functionApi = 'https://localhost:8080/api/CreateResumeCounter';

const getVisitCount = () => {
    let count = 30;
    fetch(functionApi).then(response => {
        return response.json
    }).then(response =>{
        console.log("Website called function API");
        count = response.count;
        document.getElementById("counter").innerText = count;
    }).catch(function(error){
        console.log.apply(error);
    })
    return count;
}