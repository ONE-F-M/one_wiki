frappe.ui.form.on('Wiki Page', {
    title: function(frm){
        frm.trigger('slugify');
    },
    slugify: function(frm){
        let slugify = frm.doc.title;
        slugify = slugify.toLowerCase()
        slugify = slugify.trim()
        slugify = slugify.replace(/[^\w\s-]/g, '')
        slugify = slugify.replace(/[\s_-]+/g, '-')
        slugify = slugify.replace(/^-+|-+$/g, '');
        frm.set_value('route', 'wiki/'+slugify);
    },
     refresh: function(frm) {
         if (frm.doc.__islocal != 1 && frm.doc.published == 1) {
             frm.disable_save();
             frm.toggle_display("content", false)

             frm.add_custom_button("Edit", function() {
                 var host = frappe.urllib.get_base_url();
                 let url = host + "/" + frm.doc.route + "/edit-wiki";
                 window.open(url, "_blank");
             }).addClass('btn-primary');

         }
     },
  });


  