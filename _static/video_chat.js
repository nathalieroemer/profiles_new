// prevents from using undeclared variables for example
'use strict';

// variable defined with let can be reassigned, with const not (let is often used in loops for instance)
let pc;

let startTime;
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

// e is automatically passed from javascript to the function, when event is triggered function is called
// that means here: once remoteVideo.scrcObject = streams[0] this is the case


// second
function gotRemoteStream(e) {
    if (remoteVideo.srcObject !== e.streams[0]) {
        remoteVideo.srcObject = e.streams[0];
        console.log('pc received remote stream!');
        console.log(e.streams)
    }
}


//
function makePeerConnection() {
    const configuration = {
        'iceServers': [
            {urls: 'stun:stun1.l.google.com:19302'},
            {urls: 'stun:stun2.l.google.com:19302'},
        ]
    }
// this is a interface to generate a (WebRTC) connection between the local computer and a remote peer
    // RTCConnection can receive events and may have listeners for them
    // most common event targets: element, dpcument and window
    // many support setting event handlers wia onevent properties and attributes

    pc = new RTCPeerConnection(configuration);
    // register event handler for events icecandidate, connectionstatechange and track
    // that means: when icecandidate happens, then onIceCandidate is executed, and so on
    pc.addEventListener('icecandidate', onIceCandidate);
    pc.addEventListener('connectionstatechange', onConnectionStateChange);
    pc.addEventListener('track', gotRemoteStream);

    return pc;
}

// define pc as the above function
pc = makePeerConnection();

// is executed when event 'connectionsatechange' happens if pc is called
function onConnectionStateChange(event) {
    console.log('connection state change:', pc.connectionState)
    if (pc.connectionState === 'connected') {
        console.log('peers connected!')

    }
}

let localStream;

// this happens first once the dom content is loaded
// async functions return 'Promise'
// 'Promise' can be either pending, fulfilled or rejected
// try and catch -> Anweisung die versucht werden soll, catch passiert im Fehlerfall
async function start() {

    try {
        let mediaDevices = navigator.mediaDevices;
        if (mediaDevices === undefined && window.location.href.startsWith('http:')) {
            alert("Webcam access not available on http:// URLs. If you are on Heroku, try changing the url to start with https://");
            return;
        }
        const stream = await mediaDevices.getUserMedia({audio: true, video: true});
        console.log('Received local stream');
        localVideo.srcObject = stream;
        localStream = stream;
        localStream.getTracks().forEach(track => pc.addTrack(track, localStream));

    } catch (e) {
        console.log('error:')
        console.log(e);
        alert(`Error with getUserMedia(): ${e.name}`);
    }
}

// we need this to establish the connection - its the promise in the call() function
async function liveSendVideoChat(data) {
    // namespace all messages so that it doesn't interfere with the user's other live page messages
    data.video_chat = true;
    // this makes string out of array of base-64 encoded blobs and we save them
    data.value = blobs.join();
    liveSend(data)
}

// this function sends the event candidate through the live method, once the specified candidate is reuqested to be transmitted to the remote peer
// the requested candidate is send then via livechat
async function onIceCandidate(event) {
    console.log('in onIceCandidate');
    if (event.candidate) {
        console.log('event has candidate');
         console.log(event.candidate + "is the event.candidate");
        liveSendVideoChat({type: 'ice_candidate', 'ice_candidate': event.candidate});
    }
}

// once the DOm conent has loaded, start() and call() are executed
// instead of document.addEventListener("DOMContentLoaded", function(event) { ....}); we can use =>
// await makes javascript wait until the promise settles and returns then the result
// so start() is executed when the promise in start is worked and then only the second function call() is executed
document.addEventListener("DOMContentLoaded", async (event) => {
    await start();
    await call(); // only executed when promise in start() was sucessfully returned, that is otree got the local stream
    // here we can add an await recording function
});


// once we have the local streatm, we establish the stream with the other peer
async function call() {
    startTime = window.performance.now();
    const offer = await pc.createOffer(offerOptions);
    await pc.setLocalDescription(offer);
    console.log("created offer")
    // sdp descripes the peer-to-peer connection
    liveSendVideoChat({type: 'offer', sdp: offer});
}


const offerOptions = {
    offerToReceiveAudio: 1,
    offerToReceiveVideo: 1
};

// first thing happening
function liveRecvVideoChat(data) {
    let type = data.type;
    console.log('in liveRecv:', type)
    if (type === 'answer') {
        onAnswer(data.sdp);
    }
    if (type === 'offer') {
        onOffer(data.sdp);
    }
    if (type === 'ice_candidate') {
        pc.addIceCandidate(data.ice_candidate);
    }
}

async function onOffer(desc) {
    await setRemote(desc);
    console.log('setRemoteDescription')
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
    console.log('setLocalDescription')
    liveSendVideoChat({type: 'answer', sdp: answer});
}

async function onAnswer(desc) {
    await setRemote(desc);
    console.log('set remote description');
}

async function setRemote(desc) {
    let sdp = new RTCSessionDescription(desc);
    await pc.setRemoteDescription(sdp);
}


var theStream;
var theRecorder;
var recordedChunks = [];
var reader = new FileReader();
var blobs = []

function gotMedia(stream) {
  theStream = stream;
  console.log(localVideo, "this is the local video")
  var video = localVideo;
  video.srcObject = stream;
  try {
    var recorder = new MediaRecorder(stream, {mimeType : "video/webm"});
  } catch (e) {
    console.error('Exception while creating MediaRecorder: ' + e);
    return;
  }

  theRecorder = recorder;
  recorder.ondataavailable =
      (event) => {
      reader.readAsDataURL(event.data);
        reader.onloadend = function () {
            var base64String = reader.result;
            blobs.push(base64String);
        }
      recordedChunks.push(event.data); };
  recorder.start();
}

navigator.mediaDevices.getUserMedia({video: true, audio: true})
      .then(gotMedia)
      .catch(e => { console.error('getUserMedia() failed: ' + e); });