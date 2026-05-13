const rateButton = document.querySelector("#pagerate-button")
function getLWR() {
    const loop2 = setInterval(() => {
        if (document.querySelector("#who-rated-page-area > div").textContent) {
            const whoRated = document.querySelector("#who-rated-page-area > div").textContent.replace(/(\t)| {2,}/gm,'').replace(/\n{2}|^\n|\n$/gm,'')
            console.log(whoRated);
            clearInterval(loop2)
            //put code here
            let whoRatedArray = whoRated.split('\n')
            console.log(whoRatedArray)
            whoRatedArray.forEach((value, index) => whoRatedArray[index] = value.split(/(?<=.)()(?=[+-](?:\n|$))/gm))
            console.log(whoRatedArray)
            whoRatedArray.forEach((value, index) => whoRatedArray[index].splice(1,1))
            console.log(whoRatedArray)
            //check for banned users here
            //check for non members
            
        }
    },100);
}
function bleh() {
    const loop = setInterval(()=>  {
        if (document.querySelector("#action-area").textContent.match(/Page rating/gm)) {
            const LWR = document.querySelector("#action-area > p:nth-child(5) > a")
            console.log(LWR)
            LWR.addEventListener('click', getLWR);
            clearInterval(loop);
        }
    }, 100); //swap to mutation later
}
rateButton.addEventListener('click', bleh)
