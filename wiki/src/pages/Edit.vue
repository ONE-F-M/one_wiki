<template>
    <Base>
        <div id="wiki-editor-base">
            <section class="section pb-0">
                <div class="container">
                    <div class="row">
                    
                    <div class="col-12">
                        <hr>
                            <button class="btn btn-primary float-right" @click="saveEditorData">Save</button>
                        <hr>
                        <div class="form-group row">
                            <label for="staticEmail" class="col-sm-1 col-form-label">Title</label>
                            <div class="col-sm-11">
                                <input type="text" class="form-control-plaintext" v-model="wiki.title" placeholder="Title" 
                                name="title" id="title" style="border-color:blue;">
                            </div>
                        </div>
                        <ckeditor :editor="editor" @ready="onReady" v-model="editorData" :config="editorConfig"
                            style="border-color:blue;"></ckeditor>
                        <div class="border-bottom border-default"></div>
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
    import DocumentEditor from '@ckeditor/ckeditor5-build-decoupled-document'
    import Base from './Base.vue'
    import ckConfig from '../ckConfig';

    const searchURL = new URL(window.location);

  export default {
    name: 'Edit',
    data() {
      return {
        showDialog: false,
        editor: DocumentEditor,
        editorData: ckConfig.editorData,
        editorConfig: ckConfig.editorConfig,
        // set data
        userRoles: [],
        urlKeys: {
            newdoc:searchURL.searchParams.get('wiki_page'),
            wiki_page:searchURL.searchParams.get('wiki_page'), 
            wiki_patch:searchURL.searchParams.get('wiki_patch')},
        wiki: {
            content: this.editorData,
            title: ''
        }
      }
    },
    mounted(){
      this.getRoles();
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
                    me.getWikiData();
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
            if(this.urlKeys.newdoc==1){

            } else if (this.urlKeys.wiki_page){
                let doc = createResource({url: '/api/method/one_wiki.utils.get_doc', params:{doctype:'Wiki Page', name:this.urlKeys.wiki_page}})
                doc.fetch().then(res=>{
                    me.editorData = res.content;
                    me.wiki.title = res.title;
                    $('#title').attr('disabled', true); // disabled title field since document already exists
                })
                // console.log(this.urlKeys.wiki_page)
                // let doc = createDocumentResource({doctype:'Wiki Page', name:this.urlKeys.wiki_page})
                // doc.then(res=>{
                //     console.log(res)
                // })
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
  