export default {
    name: 'ckConfig',
    editorData: '<p>Content of the editor.</p>',
    editorConfig: {
        // language: {
        //     // The UI will be English.
        //     ui: 'ar',

        //     // But the content will be edited in Arabic.
        //     content: 'ar',
        //     textPartLanguage: [
        //     { title: 'English', languageCode: 'en' },
        //     { title: 'Arabic', languageCode: 'ar' },
        //     { title: 'French', languageCode: 'fr' },
        //     { title: 'Hebrew', languageCode: 'he' },
        //     { title: 'Spanish', languageCode: 'es' }
        // ]
        // },
        ckfinder: {
            uploadUrl: `${window.location.origin}/api/method/one_wiki.utils.ckeditor_image_upload`,
            openerMethod: 'popup',
            options: {
                resourceType: 'Images'
            }
        },
        toolbar: {
            items: [
            'heading',
            '|',
            'bold',
            'italic',
            'link',
            'bulletedList',
            'numberedList',
            '|',
            'outdent',
            'indent',
            '|',
            'imageUpload',
            'blockQuote',
            'insertTable',
            'mediaEmbed',
            'undo',
            'redo',
            'alignment',
            'codeBlock',
            'fontBackgroundColor',
            'fontColor',
            'fontFamily',
            'fontSize',
            'highlight',
            'horizontalLine',
            'htmlEmbed',
            'imageInsert',
            'pageBreak',
            'removeFormat',
            'strikethrough',
            'underline',
            'style',
            'language',
            ]
        },
        language: 'en',
        image: {
            toolbar: [
            'imageTextAlternative',
            'imageStyle:inline',
            'imageStyle:block',
            'imageStyle:side',
            'imageStyle:alignLeft',
            'imageStyle:alignRight',
            'imageStyle:alignCenter',
            'imageStyle:alignBlockLeft',
            'imageStyle:alignBlockRight',
            'linkImage'
            ]
        },
        table: {
            contentToolbar: [
            'tableColumn',
            'tableRow',
            'mergeTableCells',
            'tableCellProperties',
            'tableProperties'
            ]
        },
            fontFamily: {
                options: [
                    'default',
                    'indieflowerregular',
                    'Arial, sans-serif',
                    'Verdana, sans-serif',
                    'Trebuchet MS',
                    'Apple Color Emoji',
                    'Segoe UI Emoji',
                    'Segoe UI Symbol',
                ]
            },
        licenseKey: ''
    }
}

// export default new Frappe()