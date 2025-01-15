document.addEventListener("DOMContentLoaded", function() {
    const timers = document.querySelectorAll(".timer-ribbon");

    timers.forEach(timer => {
        let startTime, interval;

        const startButton = timer.querySelector(".button-start");
        const stopButton = timer.querySelector(".button-stop");
        const pauseButton = timer.querySelector(".button-pause");

        startButton.addEventListener("click", function() {
            startTime = new Date();
            timer.dataset.state = "active";
            updateUI();

            interval = setInterval(() => {
                const elapsed = Math.floor((new Date() - startTime) / 1000);
                timer.querySelector(".elapsed-time").innerText = `${elapsed}s`;
            }, 1000);
        });

        stopButton.addEventListener("click", function() {
            clearInterval(interval);
            timer.dataset.state = "stopped";
            updateUI();
        });

        pauseButton.addEventListener("click", function() {
            clearInterval(interval);
            timer.dataset.state = "paused";
            updateUI();
        });

        function updateUI() {
            startButton.style.display = timer.dataset.state === "stopped" ? "block" : "none";
            stopButton.style.display = timer.dataset.state === "active" ? "block" : "none";
            pauseButton.style.display = timer.dataset.state === "active" ? "block" : "none";
        }
    });
});
