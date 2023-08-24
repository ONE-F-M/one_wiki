<template>
          <!-- navigation -->
          <header class="navigation fixed-top">
        <div class="container">
          <nav class="navbar navbar-expand-lg navbar-white">
            <a class="navbar-brand order-1" href="index.html">
              <img class="img-fluid" width="100px" src="/images/logo.png"
                alt="Reader | Hugo Personal Blog Template">
            </a>
            <div class="collapse navbar-collapse text-center order-lg-2 order-3" id="navigation">
              <ul class="navbar-nav mx-auto">
                <li class="nav-item dropdown">
                  <a class="nav-link" href="#" role="button" data-toggle="dropdown" aria-haspopup="true"
                    aria-expanded="false">
                    homepage <i class="ti-angle-down ml-1"></i>
                  </a>
                  <div class="dropdown-menu">
                    <router-link class="dropdown-item" to="/">Wiki Home</router-link>
                    
                    <a class="dropdown-item" href="/">Website</a>
                    
                    <a class="dropdown-item" href="/desk">Frappe Desk</a>
                
                  </div>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link" href="#" role="button" data-toggle="dropdown" aria-haspopup="true"
                    aria-expanded="false">
                    About <i class="ti-angle-down ml-1"></i>
                  </a>
                  <div class="dropdown-menu">
                    
                    <a class="dropdown-item" href="about-me.html">About Me</a>
                    
                    <a class="dropdown-item" href="about-us.html">About Us</a>
                    
                  </div>
                </li>

                <li class="nav-item">
                  <a class="nav-link" href="contact.html">Contact</a>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/edit">New Page</router-link>
                </li>

                <li class="nav-item dropdown">
                  <a class="nav-link" href="#" role="button" data-toggle="dropdown" aria-haspopup="true"
                    aria-expanded="false">Pages <i class="ti-angle-down ml-1"></i>
                  </a>
                  <div class="dropdown-menu">
                    
                    <a class="dropdown-item" href="author.html">Author</a>
                    
                    <a class="dropdown-item" href="author-single.html">Author Single</a>

                    <a class="dropdown-item" href="advertise.html">Advertise</a>
                    
                    <a class="dropdown-item" href="post-details.html">Post Details</a>
                    
                    <a class="dropdown-item" href="post-elements.html">Post Elements</a>
                    
                    <a class="dropdown-item" href="tags.html">Tags</a>

                    <a class="dropdown-item" href="search-result.html">Search Result</a>

                    <a class="dropdown-item" href="search-not-found.html">Search Not Found</a>
                    
                    <a class="dropdown-item" href="privacy-policy.html">Privacy Policy</a>
                    
                    <a class="dropdown-item" href="terms-conditions.html">Terms Conditions</a>

                    <a class="dropdown-item" href="404.html">404 Page</a>
                    
                  </div>
                </li>

                <li class="nav-item">
                  <a class="nav-link" href="shop.html">Shop</a>
                </li>
              </ul>
            </div>

            <div class="order-2 order-lg-3 d-flex align-items-center">
              <select class="m-2 border-0 bg-transparent" id="select-language">
                <option id="en" value="" selected>En</option>
                <option id="fr" value="">Fr</option>
              </select>
              
              <!-- search -->
              <form class="search-bar">
                <input id="search-query" name="s" type="search" placeholder="Type &amp; Hit Enter...">
              </form>
              
              <button class="navbar-toggler border-0 order-1" type="button" data-toggle="collapse" data-target="#navigation">
                <i class="ti-menu"></i>
              </button>
            </div>

          </nav>
        </div>
      </header>
      <!-- /navigation -->

      <!-- BODY -->
      <div class="py-4"></div>
      <slot></slot>
      <!-- BODY -->

      <footer class="footer">
      <!-- <svg class="footer-border" height="214" viewBox="0 0 2204 214" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M2203 213C2136.58 157.994 1942.77 -33.1996 1633.1 53.0486C1414.13 114.038 1200.92 188.208 967.765 118.127C820.12 73.7483 263.977 -143.754 0.999958 158.899"
          stroke-width="2" />
      </svg> -->
      
      <!-- <div class="instafeed text-center mb-5">
          <h2 class="h3 mb-4">INSTAGRAM POST</h2>
          
          <div class="instagram-slider">
            <div class="instagram-post"><img src="/images/instagram/1.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/2.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/4.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/3.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/2.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/1.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/3.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/4.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/2.jpg"></div>
            <div class="instagram-post"><img src="/images/instagram/4.jpg"></div>
          </div>
      </div> -->
      
      <div class="container">
          <div class="row align-items-center">
          <div class="col-md-5 text-center text-md-left mb-4">
              <ul class="list-inline footer-list mb-0">
                <li class="list-inline-item"><a href="privacy-policy.html">Privacy Policy</a></li>
                <li class="list-inline-item"><a href="terms-conditions.html">Terms Conditions</a></li>
              </ul>
          </div>
          <div class="col-md-2 text-center mb-4">
              <a href="index.html"><img class="img-fluid" width="100px" src="/images/logo.png" alt="Reader | Hugo Personal Blog Template"></a>
          </div>
          <div class="col-md-5 text-md-right text-center mb-4">
              <ul class="list-inline footer-list mb-0">
              
              <li class="list-inline-item"><a href="#"><i class="ti-facebook"></i></a></li>
              
              <li class="list-inline-item"><a href="#"><i class="ti-twitter-alt"></i></a></li>
              
              <li class="list-inline-item"><a href="#"><i class="ti-linkedin"></i></a></li>
              
              <li class="list-inline-item"><a href="#"><i class="ti-github"></i></a></li>
              
              <li class="list-inline-item"><a href="#"><i class="ti-youtube"></i></a></li>
              
              </ul>
          </div>
          <div class="col-12">
              <div class="border-bottom border-default"></div>
          </div>
          </div>
      </div>
      </footer>
</template>

<script>

    export default {
        name: 'Base',
        props: {
        },
        data(){
            return {
            setting: {}
            }
        },
        methods: {
            // getSetting(){
            //     this.ol.freeAPI('api/get-setting/', {}).then(res=>{
            //         if(res.data){
            //             this.setting = res.data.setting
            //             window.olSetting = res.data.setting;
            //             $('#title')[0].innerText = window.olSetting.title;
            //             if(window.olSetting.use_live_chat==true){
            //                 $('head').append(`${window.olSetting.live_chat_code}`);
            //             }
            //             $('#favicon')[0].href=`${this.url}/media/${window.olSetting.logo}`;
            //         }
            //     }).catch(error=>{
            //         console.log(error)
            //     })
            // }
        },
        computed:{
        },
        async created(){

        },
        mounted(){
            // this.getSetting();
            // // set footer year
            // let date = new Date();
            // document.querySelector("#year").innerText = date.getFullYear();
            // $('#translator')[0].src="https://translate.yandex.net/website-widget/v1/widget.js?widgetId=ytwidget&pageLang=en&widgetTheme=dark&autoMode=true"  
        },
        components: {
        // Header
        }
    }
</script>