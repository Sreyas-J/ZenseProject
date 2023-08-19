const APP_ID = "41a16d737c284fadb182676757e070ab"
const CHANNEL = sessionStorage.getItem('room')
const TOKEN = sessionStorage.getItem('token')
let UID = Number(sessionStorage.getItem('UID'))
let NAME = sessionStorage.getItem('name')

const customerKey = "cd59f667dd18444b90508cdf17105741";
const customerSecret = "188e65fe83944fad925e16fbe7f1b2f3";
const credentials = customerKey + ":" + customerSecret;
const base64Credentials = btoa(credentials);
const headers = new Headers();
headers.append("Authorization", "Basic " + base64Credentials);
headers.append("Content-Type", "application/json;charset=utf-8");

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp9' })
let localTracks = []
let remoteUsers = {}
console.log(`${TOKEN}`)

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL
    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    try {
        await client.join(APP_ID, CHANNEL, TOKEN, UID)
    } catch (error) {
        console.error(error)
        window.open('/', '_self')
    }

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    let member = createMember()

    let player = `<div class="video-container" id="user-container-${UID}">
                    <div class="username-wrapper"><span class="user-name"></span></div>
                    <div class="video-player" id="user-${UID}"></div>
                </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`);

    await client.publish([localTracks[0], localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if (mediaType === 'video') {
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null) {
            player.remove()
        }
        player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="username-wrapper"><span class="user-name">My name</span></div>
                    <div class="video-player" id="user-${user.uid}"></div>
                </div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }

    if (mediaType === 'audio') {
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leave = async () => {

    for (let i = 0; localTracks.length > i; i++) {
        localTracks[i].stop()
        localTracks[i].close()
    }
    await client.leave()
    window.open('/home/', '_self')
}

let camera = async (e) => {
    if (localTracks[1].muted) {
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    } else {
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255,80,80,1)'
    }
}

let audio = async (e) => {
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    } else {
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255,80,80,1)'
    }
}

let createMember = async () => {
    let response = await fetch('/create_member/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'name': NAME, 'room_name': CHANNEL, 'UID': UID }),
    });

    let member = await response.json();
    return member;
};


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function generateRandomUid() {
    return Math.floor(Math.random() * (Math.pow(2, 32) - 1)) + 1;
}
const uid = generateRandomUid();

const updateButtonLabel = () => {
    const button = document.getElementById('start-stop-record-btn');
    if (isRecording) {
        button.textContent = 'Stop Recording';
    } else {
        button.textContent = 'Start Recording';
    }
};

const acquireCloudRecording = async () => {
    const acquireEndpoint = `https://api.agora.io/v1/apps/${APP_ID}/cloud_recording/acquire`;

    const requestBody = {
        cname: `${CHANNEL}_${NAME}`,
        uid: uid.toString(),
        clientRequest: {
            region: "AP",
        }
    };

    const response = await fetch(acquireEndpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestBody),
    });

    if (response.ok) {
        const responseData = await response.json();
        console.log('Response data:', responseData);
        return responseData.resourceId; // Return the acquired resource ID
    } else {
        console.error('Error acquiring cloud recording resource');
        const errorResponse = await response.text(); // Get the error response as text
        console.log('Error response:', errorResponse);
        return null;
    }
};

let isRecording = false; // Track the recording state

// Function to toggle recording
const toggleRecording = async () => {
    if (isRecording === false) {
        const resourceId = await acquireCloudRecording();
        if (resourceId) {
            console.log('Resource ID acquired:', resourceId);
        } else {
            console.error('Failed to acquire resource ID');
        }
    }
    isRecording = !isRecording; // Toggle the recording state
    updateButtonLabel(); // Update the button label based on the state
};

// Attach event listener to your button
document.getElementById('start-stop-record-btn').addEventListener('click', toggleRecording)

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leave)
document.getElementById('camera-btn').addEventListener('click', camera)
document.getElementById('mic-btn').addEventListener('click', audio)