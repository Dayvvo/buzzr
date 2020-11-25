
    let sidenav = $('#sidenav');
    for(let item of document.querySelectorAll('.icon')) {
        item.addEventListener('click', ()=>{
                sidenav[0].classList.toggle('slidebar')
        }  )
    }
    

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

                setTimeout( ()=>{
                            spin()
                            } , 3500);

                setTimeout(()=>{
                        console.log(response)
                        if ($('#no_comments')) {
                            $('#no_comments').remove();
                            


                        }    

                        if (document.querySelectorAll('.comment_box').length == 4){
                            $('#commentbox').append(
                                `
                                            <button id="viewmore">
                                                <div id="view_more" data-url= "{% url 'comment_dummy' slug=article.slug %}">VIEW MORE...</div>
                                            </button>
                                        
                                        `
                            )}

                        $('#commentbox').prepend(
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
                            


                    },4200)

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
        $('#viewmore').click(()=>{ 
            click1 +=1;
            var serializeform=  $('#addcomment').serialize();
            $.ajax({
                url: $('#view_more').data('url') + click1 + '/',
                data: serializeform,
                type: 'post',
                dataType: 'json'
                
            }).done(
                function (response) {

                    let comments = ``;

                    for (let index = 0; index < response.article_set.length; index++) {
                        const element = response.article_set[index];
                        
                        for (let index2 = 0; index2 < response.dates.length; index2++) {
                            const element2 = response.dates[index];
                            
                            if (index == index2) {                                
                                comments += 
                                `
                                    <div class="comment_box">
                                        <div>
                                            <div class="comment_name"> 
                                                <h4> ${element.full_name}  </h4>  
                                            </div>
                                            <span class="comment_body">
                                                ${element.comment}
                                            </span>
                                            <div class="comment_time">                                     
                                                <sub> ${element2} </sub> 
                                            </div>
                                        </div>
                                    </div>                       
                                `       
                            }
                        }

                    }
                    
                    setTimeout(()=>{
                        $('#commentbox').append(comments)
                    },1200)

                
                }
            ).fail(
                    
                function (xhr,textstatus,errorThrown) {
                    setTimeout(
                        ()=>{
                            $('#commentbox').append(
                            '<div style="color:#db443f"  id="prompt"> Comment not sent. Check your network connection and try again </div>'
                        )},2000)
            
                    setTimeout(()=>{
                        $('#prompt').remove()

                    },3500)
                    
                }
            )



        })

