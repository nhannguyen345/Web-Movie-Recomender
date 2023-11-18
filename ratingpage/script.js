// Select all elements with the tag and store them in a Nodelist called "stars"
const stars = document.querySelectorAll(".ratingStar i");

//Loop through the "stars" Nodelist
stars.forEach((star,index1)=>{
    //Add an event listener that run a function when the "click" event is triggered
    star.addEventListener("click",()=>{
        //Loop through the "stars" NodeList Again
        stars.forEach((star,index2)=>{
            //Add the "active" class to the clicked star and any stars with a lower index
            //and remove the"active" class from any stars wwith a higher index
            index1 >= index2 ? star.classList.add("active") : star.classList.remove("active");
        });
    });
});
