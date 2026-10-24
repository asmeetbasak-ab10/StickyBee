let strikeCount = 0;
const MAX_STRIKES = 3;

// Correct Credentials
const CORRECT_USER = "AxmeetBasak";
const CORRECT_PASS = "123456";

function validateLogin() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-msg');
    const loginInterface = document.getElementById('login-interface');
    const successPage = document.getElementById('success-page');

    // SILENT LOGGING: Capture everything entered
    console.log(`[HONEYPOT LOG] Attempt ${strikeCount + 1}: User="${user}" Pass="${pass}"`);

    if (user === CORRECT_USER && pass === CORRECT_PASS) {
        // SUCCESS CASE
        loginInterface.style.display = "none";
        document.body.style.background = "#f8fafc";
        successPage.style.display = "block";
    } else {
        // FAILURE CASE
        strikeCount++;
        
        if (strikeCount >= MAX_STRIKES) {
            triggerHackerTrap();
        } else {
            errorMsg.style.display = "block";
            document.getElementById('count').innerText = MAX_STRIKES - strikeCount;
            // Clear fields for next attempt
            document.getElementById('username').value = "";
            document.getElementById('password').value = "";
        }
    }
}

function triggerHackerTrap() {
    // Completely rewrite the page body
    document.body.innerHTML = `
        <div style="background: black; color: #39FF14; height: 100vh; width: 100vw; 
                    display: flex; flex-direction: column; justify-content: center; 
                    align-items: center; font-family: 'Courier New', monospace;">
            <h1 style="font-size: 4rem; margin: 0; text-shadow: 0 0 20px #39FF14;">ACCESS DENIED</h1>
            <p style="font-size: 1.5rem; margin-top: 10px; letter-spacing: 5px;">YOU ARE BEING WATCHED</p>
            <div style="margin-top: 30px; font-size: 14px; text-align: left; opacity: 0.7;">
                > STRIKE 3 DETECTED...<br>
                > INITIATING TRACEBACK...<br>
                > PACKET CAPTURE ARCHIVED...<br>
                > IP LOGGED.
            </div>
        </div>
    `;
    document.body.style.background = "black";
}