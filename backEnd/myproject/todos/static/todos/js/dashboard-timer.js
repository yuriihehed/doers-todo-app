// Function to parse Django duration string to seconds
function parseDjangoDuration(durationString) {
    // Handle Django's duration format, e.g., "3 00:05:23" or "00:05:23"
    const parts = durationString.split(' ');
    let timeString = parts[parts.length - 1];
    let days = parts.length > 1 ? parseInt(parts[0]) : 0;
    
    const [hours, minutes, seconds] = timeString.split(':').map(Number);
    return (days * 86400) + (hours * 3600) + (minutes * 60) + seconds;
}

// Function to format seconds to 00h00m00s
function formatElapsedTime(totalSeconds) {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = Math.floor(totalSeconds % 60);
    
    return `${String(hours).padStart(2, '0')}h${String(minutes).padStart(2, '0')}m${String(seconds).padStart(2, '0')}s`;
}


class TodoTimer {
    constructor(todoId, initialTime, state) {
        this.todoId = todoId;
        this.state = state;
        this.baseSeconds = parseDjangoDuration(initialTime);
        this.startTime = Date.now();
        this.intervalId = null;
    }

    start() {
        if (this.state !== 'active') return;
        
        this.startTime = Date.now();
        this.updateDisplay();  // Make sure it's updated when started
        
        this.intervalId = setInterval(() => {
            this.updateDisplay();
            this.syncWithServer();
        }, 1000);
    }
    
    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    
        this.updateDisplay();  // Ensure it shows the formatted time when stopped
    }
    

    updateDisplay() {
        const element = document.getElementById(`elapsed-time-${this.todoId}`);
        if (!element) return;
    
        let totalSeconds = this.baseSeconds;
        
        if (this.state === 'active') {
            const elapsedSince = Math.floor((Date.now() - this.startTime) / 1000);
            totalSeconds += elapsedSince;
        }

        // Always update the display with formatted time
        element.textContent = formatElapsedTime(totalSeconds);
    }
    

    syncWithServer() {
        fetch(`/get-timer/${this.todoId}/`)
            .then(response => response.json())
            .then(data => {
                this.baseSeconds = parseDjangoDuration(data.elapsed_time);
            })
            .catch(error => console.error('Error syncing timer:', error));
    }
}

// Initialize timers when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const todoItems = document.querySelectorAll('.todo-item');
    const timers = new Map();

    todoItems.forEach(todoItem => {
        const timerRibbon = todoItem.querySelector('.timer-ribbon');
        const todoId = timerRibbon.id.replace('timer-', '');
        const state = timerRibbon.dataset.state;
        const elapsedTimeElement = todoItem.querySelector(`#elapsed-time-${todoId}`);
        
        if (elapsedTimeElement) {
            const timer = new TodoTimer(
                todoId,
                elapsedTimeElement.textContent,
                state
            );
            
            timers.set(todoId, timer);
            
            if (state === 'active') {
                timer.start();
            }
        }
    });

    // Handle state changes
    document.addEventListener('click', function(e) {
        if (!e.target.matches('.button-start, .button-stop, .button-pause')) return;
        
        const todoItem = e.target.closest('.todo-item');
        if (!todoItem) return;
        
        const todoId = todoItem.querySelector('.timer-ribbon').id.replace('timer-', '');
        const timer = timers.get(todoId);
        if (timer) {
            timer.stop();
        }
    });
});