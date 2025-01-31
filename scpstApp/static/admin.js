

function runModel() {
    console.log('runModel');

    // Get the model status div
    const modelStatus = document.getElementById('modelStatus');
    if (modelStatus) {
        modelStatus.innerText = 'Model Running ...';
    }
    else {
        console.log('modelStatus not found');
    }

    // Get the license plate text div
    const licensePlateText = document.getElementById('licensePlateText');
    if (licensePlateText) {
        licensePlateText.innerText = 'None';
    }
    else {
        console.log('licensePlateText not found');
    }

    // Make a request to the server to run the model
    fetch('/runModel')
        .then(response => {
            if (response.status === 501) {
                throw new Error('Server error: Model execution failed');
            }
            return response.json();
        })
        .then(data => {
            console.log('Model page (hopefully) opened successfully');
            //console.log(data);
            if (modelStatus && licensePlateText) {
                modelStatus.innerText = 'Model Run Successfully!';
                licensePlateText.innerText = data.licensePlate;
            }
            else {
                console.log('modelStatus or licensePlateText not found');
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
            if (modelStatus) {
                modelStatus.innerText = 'Error: ' + error.message;
            }
            if (licensePlateText) {
                licensePlateText.innerText = 'Error occurred';
            }
        });
}

// Function that gets and displays the user list
function getUserList() {
    console.log('getUserList');

    fetch('/users')
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log('User list retrieved successfully');
            // Update userList div
            const userList = document.getElementById('userList');
            if (userList) {
                userList.innerHTML = `
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Users</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Email</th>
                                            <th>License Plate</th>
                                            <th>Last Entry</th>
                                            <th>Last Exit</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${data.map(user => `
                                            <tr>
                                                <td>${user.name}</td>
                                                <td>${user.email}</td>
                                                <td>${user.license_plate}</td>
                                                <td>${user.last_entry}</td>
                                                <td>${user.last_exit}</td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                `;
            }
            else {
                console.log('No Users Found');
            }
        });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded');

    var modelRunning = false;

    // Get the run model button
    const toggleModelBtn = document.getElementById('toggleModelBtn');
    toggleModelBtn.addEventListener('click', () => {
        modelRunning = !modelRunning;
        if (modelRunning) {
            toggleModelBtn.innerText = 'Stop Model';
        }
        else {
            toggleModelBtn.innerText = 'Start Model';
        }
    });

    // Function to update countdown timer
    function updateCountdown(endTime) {
        const now = new Date().getTime();
        const timeLeft = endTime - now;
        
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        
        const nextRunP = document.getElementById('nextRun');
        if (nextRunP) {
            nextRunP.textContent = `Next run in: ${minutes}m ${seconds}s`;
        }
    }

    // Function to handle periodic model runs
    function startPeriodicRuns() {
        const interval = 30 * 1000; // 30 seconds in milliseconds
        const nextRunTime = new Date().getTime() + interval;
        
        // Update countdown every second
        const countdownInterval = setInterval(() => {
            updateCountdown(nextRunTime);
        }, 1000);

        // Run model every 3 minutes
        setTimeout(() => {
            if (modelRunning) {
                runModel();
            }
            getUserList();
            clearInterval(countdownInterval);
            startPeriodicRuns(); // Restart the cycle
        }, interval);
    }

    // Start periodic runs
    startPeriodicRuns();

});

