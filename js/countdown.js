
export function createCountdown(dateString) {
    const targetDate = new Date(dateString).getTime();

    const countdownDiv = document.createElement("div");
    countdownDiv.id = "countdown-timer";
    countdownDiv.innerText = "I muess hurti rächne...";

    // Find the container element automatically if a string ID is passed
    const container = document.getElementById("map");
    console.log(`Adding Countdown to map container ${container}`);
    container.appendChild(countdownDiv);

    const countdownFunction = setInterval(() => {
        //console.log('Updating Countdown...')
        const now = new Date().getTime();
        const distance = targetDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        console.log(`${days}/${hours}/${minutes}/${seconds}`)
        
        var day_text = '';
        var hour_text = '';

        
        if (days < 1){
            day_text = ``;
        }
        else if (days < 2) {
            day_text = `${days} Tag`;
        } else {
            day_text = `${days} Täg`;
        };

        if (hours < 1){
            hour_text = ``;
        }
        else if (hours < 2){
            hour_text = `${hours} Stund`;
        } else {
            hour_text = `${hours} Stunde`;
        }

        const innerTHeader = 'Es geit no'

        const innerText = `${innerTHeader}\n ${day_text} ${hour_text} ${minutes} Minute ${seconds} Sekunde`
        //console.log(innerText)
        countdownDiv.innerText = innerText;

        if (distance < 0) {
            clearInterval(countdownFunction);
            countdownDiv.innerText = "Itz ischs düre, mir heis gnosse :)";
        }
        }, 1000);

  return countdownDiv;
}
