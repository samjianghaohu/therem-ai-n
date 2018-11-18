var posX;
var play;

var vw = document.documentElement.clientWidth;
var vh = document.documentElement.clientHeight;

var canvas;

var ampEnv = new Tone.AmplitudeEnvelope({
    "attack": 0.1,
    "decay": 0.2,
    "sustain": 0.1,
    "release": 0.5
}).toMaster();

var thereminSynth = new Tone.DuoSynth({
    harmonicity: 2,
    vibratoAmount: 0.1,
    voice0: {
        oscillator: {
            type: "sine"
        }
    },
    voice1: {
        oscillator: {
            type: "sine"
        }
    }
}).toMaster();

function midiLoad(){
    MidiConvert.load("midfile/returning.mid", function(midi){
        console.log("load successful");
        console.log(midi);

        // Tone.Transport.bpm.value = midi.header.bpm;
        Tone.Transport.bpm.value = 120;
        midiPart = new Tone.Part(function(time, note){
            thereminSynth.portamento = 0.5;
            // thereminSynth.connect(ampEnv);
            thereminSynth.triggerAttackRelease(note.name, note.duration, time, note.velocity)
        }, midi.tracks[1].notes);
        Tone.Transport.start();
        midiPart.start();
    });
}


function midiPlay(){
    midiLoad();
}

function startMidiFile(){
    console.log("Midi file start");
    midiPlay();
}

function startSynth(noteFromMidi) {
    thereminSynth.triggerAttack();
    console.log("started");
}

function setSynthNote(noteFromMidi){
    thereminSynth.portamento = 1;
    thereminSynth.setNote(noteFromMidi);
}
function stopSynth() {
    thereminSynth.triggerRelease();
    console.log("stopped");

}


//for testing the glide/portamento stuff
function getMouseCoord() {
    posX = event.clientX;

    if (posX > vw/2){
        let noteFromMidi = Tone.Frequency(64, "midi").toNote();
        setSynthNote(noteFromMidi)
    }else{
        let noteFromMidi = Tone.Frequency(70, "midi").toNote();
        setSynthNote(noteFromMidi)
    }
}

var meter;
var smoothedLevel;

function setup(){
    canvas = createCanvas(vw, vh);
    frameRate(60);
    background(200, 120 ,120);
    meter = new Tone.Meter();
    thereminSynth.connect(meter);
}

function draw(){
    background(200, 120 ,120);
    level = meter.getValue();
    level = abs(level);
    fill(120, 200, 120);
    noStroke();
    ellipse(width/2, height/2, level * 400, level * 400);
}

function keyTyped(){
    if (key === 'p'){
        midiPlay();
    }
}

// window.onresize = function(){
//     var screenWidth  = window.innerWidth;
//     var screenHeight = window.innerHeight;
//     canvas.size(screenWidth, screenHeight);
// }
