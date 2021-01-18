let canvas = document.querySelector("canvas");
let c = canvas.getContext('2d');

let x = 0;
let y = 0;

let points = [];
let obsticles = [];

function makeCanvas(x,y){
    canvas.width = window.innerWidth/2;
    canvas.height = window.innerWidth/2*(y/x);
}

function grid(x,y){
    width = canvas.width / x;
    height = canvas.height/ y;
    for(let i= 0; i<= x; i++){
        for(let j =0; j<= y; j++){
            c.beginPath();
            c.rect(width*i,height*j, width, height);
            c.stroke();
        }
    }
}

function addPoints(){
    myPoints= '[';
    for(i in points){
        myPoints += '('+  points[i][0].toString() +','+  points[i][1].toString() +')';
        if(points.length-1 != i){
            myPoints+=','
        }
    }
    myPoints += ']';

    myObsticles= '[';
    for(i in obsticles){
        myObsticles += '('+  obsticles[i][0].toString() +','+  obsticles[i][1].toString() +')';

        console.log([obsticles.length-1, i]);
        if(obsticles.length-1 != i){
            myObsticles+=','
        }
    }
    myObsticles += ']';

    document.getElementById('test').innerHTML = "<form method= 'POST'> Points <input type= 'text' name = 'points' value =" +myPoints+"> Obsticles <input type= 'text' name = 'obsticles' value =" +myObsticles+"><input type = 'submit'></form>";
}

function gridUpdate(event){
    console.log("b");
    width = canvas.width / x;
    height = canvas.height/ y;
    for(let i= 0; i<= x; i++){
        for(let j =0; j<= y; j++){
            c.beginPath();
            c.fillStyle = 'black';
            c.rect(width*i,height*j, width, height);
            if(event.offsetX>=width*i && event.offsetX<width*(i+1)
            && event.offsetY>= height*j && event.offsetY < height*(j+1)){
                c.fill();
                points.push([i,j])
                addPoints();

            }
            else{
                 c.stroke();
            }
        }
    }
}

function gridUpdateObsticle(event){
    console.log("obstic")
    width = canvas.width / x;
    height = canvas.height/ y;
    for(let i= 0; i<= x; i++){
        for(let j =0; j<= y; j++){
            c.beginPath();
            c.fillStyle = 'red';
            c.rect(width*i,height*j, width, height);
            if(event.offsetX>=width*i && event.offsetX< width*(i+1)
            && event.offsetY>= height*j && event.offsetY < height*(j+1)){
                c.fill();
                obsticles.push([i,j]);
                addPoints();
            }
            else{
                 c.stroke();
            }
        }
    }
}


function removeUpdate(event){
    console.log("remove");
    width = canvas.width / x;
    height = canvas.height/ y;
    for(let i= 0; i<= x; i++){
        for(let j =0; j<= y; j++){
            c.beginPath();
            c.fillStyle = 'azure';
            c.rect(width*i,height*j, width, height);
            if(event.offsetX>=width*i && event.offsetX< width*(i+1)
            && event.offsetY>= height*j && event.offsetY < height*(j+1)){
                c.fill();
            }
            else{
                 c.stroke();
            }
        }
    }
}


//setting gridSize:
let submit = document.getElementById('submit');
submit.addEventListener('click',function(){
    let myWidth = document.getElementById('width').value; // i meter
    let myHeight =document.getElementById('height').value;
    makeCanvas(myWidth,myHeight);
    x= myWidth*2; //500 mm i bredde og høyde
    y = myHeight*2;
    grid(x,y);
})



let point = document.getElementById('point');
let obstacle = document.getElementById('obstacle');
let remove = document.getElementById('remove');

let finalSubmit = document.getElementById('finalSubmit')

function pointEvent(){
    canvas.removeEventListener('mousedown', gridUpdateObsticle);
    canvas.removeEventListener('mousedown', removeUpdate);
    canvas.addEventListener('mousedown',gridUpdate);
}

function obsticleEvent(){
    canvas.removeEventListener('mousedown', gridUpdate);
    canvas.removeEventListener('mousedown', removeUpdate);
    canvas.addEventListener('mousedown', gridUpdateObsticle);
}

function removeEvent(){
    canvas.removeEventListener('mousedown', gridUpdate);
    canvas.removeEventListener('mousedown', gridUpdateObsticle);
    canvas.addEventListener('mousedown', removeUpdate);
}
point.addEventListener('click',pointEvent);
obstacle.addEventListener('click', obsticleEvent);
remove.addEventListener('click', removeEvent);

finalSubmit.addEventListener('click', function(){
    myList= '[';
    for(i in points){
        myList += '('+  points[i][0].toString() +','+  points[i][1].toString() +')';
        if(points.length-1 != i){
            myList+=','
        }
    }
    myList += ']';
    document.getElementById('test').innerHTML = "<form method= 'POST'> framework <input type= 'text' name = 'framework' value =" +myList+"><input type = 'submit'></form>";
})