<template>
    <Base>
        <div id="wiki-editor-base">
            
            <section class="section-sm">
                <div class="container">
                    <div class="row justify-content-center">
                        <aside class="col-lg-4 @@sidebar">
                            <!-- categories -->
                            <div class="widget widget-categories">
                                <h4 class="widget-title"><span>Categories</span></h4>
                                <ul class="list-unstyled widget-list">
                                <li><a href="tags.html" class="d-flex">Creativity <small class="ml-auto">(4)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Demo <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Elements <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Food <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Microwave <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Natural <small class="ml-auto">(3)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Newyork city <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Nice <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Tech <small class="ml-auto">(2)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Videography <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Vlog <small class="ml-auto">(1)</small></a></li>
                                <li><a href="tags.html" class="d-flex">Wondarland <small class="ml-auto">(1)</small></a></li>
                                </ul>
                            </div><!-- tags -->
                            <div class="widget">
                                <h4 class="widget-title"><span>Tags</span></h4>
                                <ul class="list-inline widget-list-inline widget-card">
                                <li class="list-inline-item"><a href="tags.html">City</a></li>
                                <li class="list-inline-item"><a href="tags.html">Color</a></li>
                                <li class="list-inline-item"><a href="tags.html">Creative</a></li>
                                <li class="list-inline-item"><a href="tags.html">Decorate</a></li>
                                <li class="list-inline-item"><a href="tags.html">Demo</a></li>
                                <li class="list-inline-item"><a href="tags.html">Elements</a></li>
                                <li class="list-inline-item"><a href="tags.html">Fish</a></li>
                                <li class="list-inline-item"><a href="tags.html">Food</a></li>
                                <li class="list-inline-item"><a href="tags.html">Nice</a></li>
                                <li class="list-inline-item"><a href="tags.html">Recipe</a></li>
                                <li class="list-inline-item"><a href="tags.html">Season</a></li>
                                <li class="list-inline-item"><a href="tags.html">Taste</a></li>
                                <li class="list-inline-item"><a href="tags.html">Tasty</a></li>
                                <li class="list-inline-item"><a href="tags.html">Vlog</a></li>
                                <li class="list-inline-item"><a href="tags.html">Wow</a></li>
                                </ul>
                            </div><!-- recent post -->
                            
                            <!-- Social -->
                            <div class="widget">
                                <h4 class="widget-title"><span>Social Links</span></h4>
                                <ul class="list-inline widget-social">
                                <li class="list-inline-item"><a href="#"><i class="ti-facebook"></i></a></li>
                                <li class="list-inline-item"><a href="#"><i class="ti-twitter-alt"></i></a></li>
                                <li class="list-inline-item"><a href="#"><i class="ti-linkedin"></i></a></li>
                                <li class="list-inline-item"><a href="#"><i class="ti-github"></i></a></li>
                                <li class="list-inline-item"><a href="#"><i class="ti-youtube"></i></a></li>
                                </ul>
                            </div>
                        </aside>
                        <div class="col-lg-8 mb-5 mb-lg-0">
                            <h2 class="h5 section-title">{{ wiki.title }}</h2>
                                    
                            <article class="card mb-4">
                                <div class="row card-body">
                                <div class="col-12">
                                    <h3 class="h4 mb-3"><a class="post-title" href="post-details.html">{{ wiki.title }}</a></h3>
                                    <ul class="card-meta list-inline">
                                    <li class="list-inline-item">
                                        <a href="author-single.html" class="card-meta-author">
                                        <img src="/images/kate-stone.jpg" alt="Kate Stone">
                                        <span>Kate Stone</span>
                                        </a>
                                    </li>
                                    <li class="list-inline-item">
                                        <i class="ti-timer"></i>2 Min To Read
                                    </li>
                                    <li class="list-inline-item">
                                        <i class="ti-calendar"></i>14 jan, 2020
                                    </li>
                                    <li class="list-inline-item">
                                        <ul class="card-meta-tag list-inline">
                                        <li class="list-inline-item"><a href="tags.html">Wow</a></li>
                                        <li class="list-inline-item"><a href="tags.html">Tasty</a></li>
                                        </ul>
                                    </li>
                                    </ul>
                                    <p id="wiki-content"></p>
                                    <a href="post-details.html" class="btn btn-outline-primary">Read More</a>
                                </div>
                                </div>
                            </article>
                
            
                            <ul class="pagination justify-content-center">
                                <li class="page-item page-item active ">
                                    <a href="#!" class="page-link">1</a>
                                </li>
                                <li class="page-item">
                                    <a href="#!" class="page-link">2</a>
                                </li>
                                <li class="page-item">
                                    <a href="#!" class="page-link">&raquo;</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </Base>
  </template>
  
  <script>
    import { Dialog, frappeRequest, createResource, createDocumentResource } from 'frappe-ui'
    import Swal from 'sweetalert2'
    import Base from './Base.vue'
    
  export default {
    name: 'WikiDetail',
    data() {
      return {
        showDialog: false,
        userRoles: [],
        wiki: {
            title: ''
        }
      }
    },
    mounted(){
      this.getRoles();
      this.getWikiData();
      console.log(this.$route.params)
    console.log('vue')
    },
    beforeUnmount() {
    },
    methods: {
        getRoles(){
            let me = this;
            let fetchURL = createResource({url: '/api/method/one_wiki.utils.get_roles'})
            fetchURL.fetch().then((data)=>{
                me.userRoles = data;
                if (me.userRoles.includes('Wiki Editor') || me.userRoles.includes('Wiki Manager')){
                    
                } else {
                    $('#wiki-editor-base').hide()
                    Swal.fire(
                        'Error',
                        'Invalid Link',
                        'warning'
                    )
                }
                
            })
        },
        setUrl(){
            let me = this;
            let fetchURL = createResource({
                url: '/api/method/one_wiki.utils.get_url',
            })
            fetchURL.fetch().then((data)=>{
                // me.editorConfig.ckfinder.uploadUrl = `${data}/api/method/one_wiki.utils.ckeditor_image_upload`
            })
        },
        getWikiData(){
            let me =this;
            if(me.$route.params.pk != null){
                let doc = createResource({url: '/api/method/one_wiki.utils.get_doc', params:{doctype:'Wiki Page', name:me.$route.params.pk}})
                doc.fetch().then(res=>{
                    if (res.code==404){
                        $('#wiki-editor-base').hide()
                        Swal.fire(
                            'Error',
                            res.text,
                            'warning'
                        )
                    } else {
                        me.wiki = res.data;
                        $('#wiki-content').html(me.wiki.content);
                    }
                })
            } else {
                $('#wiki-editor-base').hide()
                Swal.fire(
                    'Error',
                    'Invalid Link',
                    'warning'
                )
            }
        },
        onReady( editor )  {
            let me = this;
            // Insert the toolbar before the editable area.
            editor.ui.getEditableElement().parentElement.insertBefore(
                    editor.ui.view.toolbar.element,
                    editor.ui.getEditableElement()
            );
        },
        saveEditorData(){
            console.log(this.editorData)
        }
    },
    resources: {
      ping: {
        url: 'ping',
      },
    },
    components: {
      Dialog,
      Base,
    },
  }
  </script>
  