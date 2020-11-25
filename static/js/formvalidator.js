    window.addEventListener('lo',() =>{
    })
    let windowlocation = window.location.href.split('/')[window.location.href.split('/').length - 2]        

    let pagelink = document.querySelectorAll('.pag_link');    
    document.onreadystatechange= ()=>{
        
        if (document.readyState==='complete') {
                for(const a of pagelink){
                    let windowlocation = window.location.href.split('/')[window.location.href.split('/').length - 2]
                    if (a.firstElementChild.textContent === windowlocation || a.href === window.location.href ) {
                            a.classList.toggle('paginate_active') ;                       
                        }

                        $('#navsections a').each( function(){
                                let self = this;
                                self2 = self.href.split('/')[self.href.split('/').length - 2];
                                if (self2 == a.parentElement.className){
                                        self.classList.add('aCtive')
                    
                    
                        }}
                        )
                    
                        
                }
                
                

        }       
    }
        for (const a of pagelink){
                a.addEventListener('click',(e)=>{    
                            if (a.classList.contains('paginate_active')) {
                                  e.preventDefault();
                            }               
                })

        }

    // let navlinks = document.querySelectorAll('#navsections >a'); 
    // for(const a of navlinks){
    //     a.addEventListener('click',()=>{
    //             a.classList.toggle('aCtive');
    //             for (const a3 of navlinks) {
    //                 if (a3.innerHTML !==a.innerHTML && a3.classList.contains('aCtive') ) {
    //                     a3.classList.add('aCtive');
    //                 }
    //             }
                  
            
    //     })
    // }

    let commentform = document.querySelector('#addcomment')
        commentform.addEventListener('submit', (e)=>{
            e.preventDefault()
            function spin() {
                let spinner = document.querySelector('.span2');
                spinner.classList.toggle('spin');
            }
            spin()
            var serializeform=  $('#addcomment').serialize()
            $('#addcomment')[0].reset()
            $.ajax({
              url: $('#addcomment').data('url'),
              data: serializeform,
              type: 'post',
              dataType: 'json' 
                         


        }).done(
            function (response) {

                setTimeout(spin(), 4500);

                setTimeout(()=>{
                        console.log(response)
                        if ($('#no_comments')) {
                            $('#no_comments').remove();
                            


                        }

                        $('#commentbox').append(
                            `
                            <div class="comment_box">
                                <div>
                                    <div class="comment_name"> 
                                        <h4> ${response.comments.full_name}  </h4>  
                                    </div>
                                    <span class="comment_body">
                                        ${response.comments.comment}
                                    </span>
                                    <div class="comment_time">                                     
                                        <sub> ${response.date_time} </sub> 
                                    </div>
                                </div>
                            </div>

                            `                            
                        );
                            
                    // else if (response.exception) {
                    //     $('#addcomment').append(
                    //         '<div style="background:#db443f"  id="prompt"> Comment not sent. Check your network connection and try again </div>'
                    //     );
                        
                    // }
                    // (
                    //     ()=>{
                    //         setTimeout(()=>{
                    //             $('#prompt').remove()
                    //         },3200) 

                    //     }
                    // )()

                },5000)

            }

        ).fail(            
                function (xhr,textstatus,errorThrown) {
                    setTimeout(
                        ()=>{
                            spin()
                            $('#addcomment').append(
                            '<div style="color:#db443f"  id="prompt"> Comment not sent. Check your network connection and try again </div>'
                        )},2000)
            
                    setTimeout(()=>{
                        $('#prompt').remove()

                    },3500) 
   
                }
                
        

    

        )


        })

     
        click1 = 1;
        $('.viewmore')[0].click(()=>{ 
            click1 +=1;
            serializeform = ('#addcomment').serialize();
            $.ajax({
                url: $('#view_more').data('url') + click1,
                data: serializeform,
                type: 'post',
                dataType: 'json'
                
            }).done(
                function (response) {
                    let comments = ``;
                    for (const i of response.article_set) {
                        
                        comments += 
                        `
                            <div class="comment_box">
                                <div>
                                    <div class="comment_name"> 
                                        <h4> ${i.full_name}  </h4>  
                                    </div>
                                    <span class="comment_body">
                                        ${i.comments.comment}
                                    </span>
                                    <div class="comment_time">                                     
                                        <sub> ${i.date_time} </sub> 
                                    </div>
                                </div>
                            </div>                       
                        `

                    }
                    
                    $('#commentbox').append(comments)
                
                }
            )



        })

