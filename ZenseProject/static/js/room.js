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
var sid=null
var resourceId=null
var rec_uid=null

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

let isRecording = false; // Track the recording state
const uid = generateRandomUid().toString();
const cname=`${CHANNEL}_${NAME}`;

function generateRandomUid() {
    return Math.floor(Math.random() * (Math.pow(2, 32) - 1)) + 1;
}

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
        cname: cname,
        uid: uid,
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
        return responseData // Return the acquired resource ID
    } else {
        console.error('Error acquiring cloud recording resource');
        const errorResponse = await response.text(); // Get the error response as text
        console.log('Error response:', errorResponse);
        return null;
    }
};

// Function to start cloud recording
const startCloudRecording = async (resourceId,rec_uid) => {
    console.log("resource id: ",resourceId," , app id: ",APP_ID)
    const startEndpoint = `https://api.agora.io/v1/apps/${APP_ID}/cloud_recording/resourceid/${resourceId}/mode/mix/start`;

    const requestBody = {
        uid: rec_uid.toString(),
        cname: `${CHANNEL}_${NAME}`, 
        clientRequest: {
            token: TOKEN,
            recordingConfig: {
                maxIdleTime:30,
                streamTypes:2,
                audioProfile:1,
                channelType: 0,
                videoStreamType:0,
                transcodingConfig: {
                    "height": 640,
                    "width": 360,
                    "bitrate": 500,
                    "fps": 15,
                    "mixedVideoLayout": 1,
                    "backgroundColor": "#FF0000"
                },
            },
            storageConfig: {
                accessKey: "AKIAY74HYE7CAGCY6KUC",
                region: 14,
                bucket: "zense-project-videocall-recording",
                secretKey: "XvoA9I+CyHsWb+qnDll4mQNGvlwCLDorVVnZ7jkY",
                vendor: 1,
            }
        }
    };
    console.log("body: ",JSON.stringify(requestBody))

    const response = await fetch(startEndpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestBody),
    });

    if (response.ok) {
        const responseData = await response.json();
        sid=responseData['sid']
        console.log('Recording started:', sid);
        return sid
    } else {
        console.error('Error starting cloud recording');
        const errorResponse = await response.text(); // Get the error response as text
        console.log('Error response:', errorResponse);
    }
    return null
};


const stopCloudRecording = async (sid,resourceId,rec_uid) => {
    const stopEndpoint = `https://api.agora.io/v1/apps/${APP_ID}/cloud_recording/resourceid/${resourceId}/sid/${sid}/mode/mix/stop`;

    const requestBody = {
        cname: cname,
        uid: rec_uid,
        clientRequest: {}
    };

    const response = await fetch(stopEndpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestBody),
    });

    if (response.ok) {
        console.log('Recording stopped successfully');
    } else {
        console.error('Error stopping cloud recording');
        const errorResponse = await response.json(); // Get the error response as JSON
        console.log('Error response:', errorResponse);
    }
};

// Attach event listener to your "Start Recording" button
document.getElementById('start-stop-record-btn').addEventListener('click', async () => {
    if (isRecording === false) {
        const data = await acquireCloudRecording();
        resourceId= data.resourceId;
        rec_uid=data.uid
        if (resourceId) {
            console.log('Resource ID acquired:', resourceId);
            sid=await startCloudRecording(resourceId,rec_uid); // Start recording after acquiring resource ID
        } else {
            console.error('Failed to acquire resource ID');
        }
    }
    else{
        stopCloudRecording(sid,resourceId,rec_uid);
    }
    isRecording = !isRecording; // Toggle the recording state
    updateButtonLabel(); // Update the button label based on the state
});

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leave)
document.getElementById('camera-btn').addEventListener('click', camera)
document.getElementById('mic-btn').addEventListener('click', audio)