(()=>{window.EditAsset=class{constructor(){this.make_code_field_group(),this.add_attachment_popover(),this.set_code_editor_height(),this.render_preview(),this.add_attachment_handler(),this.set_listeners(),this.create_comment_box(),this.make_title_editable(),this.render_sidebar_diff()}make_code_field_group(){this.code_field_group=new frappe.ui.FieldGroup({fields:[{fieldname:"type",fieldtype:"Data",default:"Rich Text",options:"Rich Text"},{fieldtype:"Section Break"},{fieldname:"code_html",fieldtype:"Text Editor",default:$(".wiki-content-html").html(),depends_on:'eval:doc.type=="Rich Text"'}],body:$(".wiki-write").get(0)}),this.code_field_group.make(),$(".wiki-write .form-section:last").removeClass("empty-section")}get_attachment_controls_html(){return`
			<div class="attachment-controls">
				<div class="show-attachments" tabindex="-1" data-trigger="focus">
					${this.get_show_uploads_svg()}
					<span class="number">0</span> attachments
				</div>
				<div class="add-attachment-wiki">
					<span class="btn">
						${this.get_upload_image_svg()}
						Upload Attachment
					</span>
				</div>
			</div>
		`}get_show_uploads_svg(){return`<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path d="M12.6004 6.68841L7.6414 11.5616C6.23259 12.946 3.8658 12.946 2.45699 11.5616C1.04819 10.1772
			1.04819 7.85132 2.45699 6.4669L6.85247 2.14749C7.86681 1.15071 9.44467 1.15071 10.459 2.14749C11.4733
			3.14428 11.4733 4.69483 10.459 5.69162L6.40165 9.62339C5.83813 10.1772 4.93649 10.1772 4.42932 9.62339C3.8658
			9.06962 3.8658 8.18359 4.42932 7.68519L7.81045 4.36257" stroke="#2D95F0" stroke-miterlimit="10" stroke-linecap="round"/>
		</svg>`}get_upload_image_svg(){return`<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path d="M8 14.5C11.5899 14.5 14.5 11.5899 14.5 8C14.5 4.41015 11.5899 1.5 8 1.5C4.41015 1.5 1.5 4.41015 1.5 8C1.5 11.5899
			 4.41015 14.5 8 14.5Z" stroke="#505A62" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
			<path d="M8 4.75V11.1351" stroke="#505A62" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
			<path d="M5.29102 7.45833L7.99935 4.75L10.7077 7.45833" stroke="#505A62" stroke-miterlimit="10" stroke-linecap="round"
			stroke-linejoin="round"/>
		</svg>`}add_attachment_popover(){$(".show-attachments").popover({placement:"bottom",content:()=>this.build_attachment_table(),html:!0})}build_attachment_table(){var e=$('<div class="wiki-attachment"></div>');e.empty();var a=$(this.get_attachment_table_header_html()).appendTo(e);if(!this.attachments||!this.attachments.length)return"No attachments uploaded";let i=t=>t.split("/").pop().split(".").slice(0,-1).join(".").replaceAll("_"," ").replaceAll("-"," ");return this.attachments.forEach(t=>{let s=$("<tr></tr>").appendTo(a.find("tbody"));$(`<td>${t.file_name}</td>`).appendTo(s),$(`<td>
			<a class="btn btn-default btn-xs btn-primary-light text-nowrap copy-link" data-link="![${i(t.file_url)}](${t.file_url})" data-name = "${t.file_name}" >
				Copy Link
			</a>
			</td>`).appendTo(s),$(`<td>

			<a class="btn btn-default btn-xs  center delete-button"  data-name = "${t.file_name}" >
			<svg class="icon icon-sm"><use xlink:href="#icon-delete"></use></svg>

			</a>
			</td>`).appendTo(s)}),e}get_attachment_table_header_html(){return`<table class="table  attachment-table" ">
			<tbody></tbody>
		</table>`}set_code_editor_height(){setTimeout(()=>{let e=this.code_field_group.get_field("code_md");e.expanded=!this.expanded,e.refresh_height(),e.toggle_label()},120)}raise_patch(e=!1){var a={};let i=$(".doc-sidebar .web-sidebar").get(0).dataset.name;a[i]=[];let t=$($(".doc-sidebar .web-sidebar").get(0)).children(".sidebar-items").children("ul").not(".hidden").children("li");t.each(n=>{!t[n].dataset.name||a[i].push({name:t[n].dataset.name,type:t[n].dataset.type,new:t[n].dataset.new,title:t[n].dataset.title,group_name:t[n].dataset.groupName})}),$('.doc-sidebar [data-type="Wiki Sidebar"]').each(function(){let n=$(this).get(0).dataset.groupName;a[n]=[];let o=$(this).children("ul").children("li");o.each(p=>{!o[p].dataset.name||a[n].push({name:o[p].dataset.name,type:o[p].dataset.type,new:o[p].dataset.new,title:o[p].dataset.title,group_name:o[p].dataset.groupName})})});var s=this,l=[];let d=$(".edit-title span").text();l.push({fieldname:"edit_message",fieldtype:"Text",label:"Message",default:$('[name="new"]').val()?`Add new page: ${d}`:`Edited ${d}`,mandatory:1},{fieldname:"sidebar_edited",fieldtype:"Check",label:"I updated the sidebar",default:$('[name="new"]').val()?1:0});let r=new frappe.ui.Dialog({fields:l,title:__("Please describe your changes"),primary_action_label:__("Submit Changes"),primary_action:function(){frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.update",args:{name:$('[name="wiki_page"]').val(),wiki_page_patch:$('[name="wiki_page_patch"]').val(),message:this.get_value("edit_message"),sidebar_edited:this.get_value("sidebar_edited"),content:s.content,type:s.code_field_group.get_value("type"),attachments:s.attachments,new:$('[name="new"]').val(),title:$(".edit-title span").text(),new_sidebar:$(".doc-sidebar").get(0).innerHTML,new_sidebar_items:a,draft:e||null},callback:n=>{!n.message.approved&&n.message.route=="contributions"?frappe.msgprint({message:"A Change Request has been created. You can track your requests on the contributions page",indicator:"green",title:"Change Request Created",alert:1}):!n.message.approved&&n.message.route=="drafts"&&frappe.msgprint({message:"Draft Saved",indicator:"green",title:"Change Request Created",alert:1}),window.location.href="/"+n.message.route},freeze:!0}),r.hide(),$("#freeze").addClass("show")}});r.show()}render_preview(){$('a[data-toggle="tab"]').on("click",e=>{let a=$(e.target);if(a.prop("id")==="preview-tab"||a.prop("id")==="diff-tab"){let t=$(".wiki-preview"),s=$(".wiki-diff"),l=this.code_field_group.get_value("type"),d="";if(l=="Markdown")d=this.code_field_group.get_value("code_md");else{d=this.code_field_group.get_value("code_html");var i=new TurndownService;i=i.keep(["div class","iframe"]),d=i.turndown(d)}if(!d){this.set_empty_message(t,s);return}this.set_loading_message(t,s),frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.preview",args:{content:d,type:l,path:this.route,name:$('[name="wiki_page"]').val(),attachments:this.attachments,new:$('[name="new"]').val()},callback:r=>{if(r.message&&(t.html(r.message.html),!$('[name="new"]').val())){let n='<div class="text-muted center"> No Changes made</div>',o=$(r.message.diff).find(".insert, .delete").length?r.message.diff:n;s.html(o)}}})}})}set_empty_message(e,a){e.html("<div>Please add some code</div>"),a.html("<div>Please add some code</div>")}set_loading_message(e,a){e.html("Loading preview..."),a.html("Loading diff...")}add_attachment_handler(){var e=this;$(".add-attachment-wiki").click(function(){e.new_attachment()}),$(".submit-wiki-page").click(function(){e.get_markdown()}),$(".draft-wiki-page").click(function(){e.get_markdown(!0)})}new_attachment(){this.dialog&&this.dialog.$wrapper.remove(),new frappe.ui.FileUploader({folder:"Home/Attachments",on_success:e=>{this.attachments||(this.attachments=[]),this.save_paths||(this.save_paths={}),this.attachments.push(e),$(".wiki-attachment").empty().append(this.build_attachment_table()),$(".attachment-controls").find(".number").text(this.attachments.length)}})}get_markdown(e=!1){var a=this;a.code_field_group.get_value("type")=="Markdown"?(this.content=a.code_field_group.get_value("code_md"),this.raise_patch(e)):(this.content=this.code_field_group.get_value("code_html"),frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.extract_images_from_html",args:{content:this.content},callback:i=>{if(i.message){a.content=i.message;var t=new TurndownService;t=t.keep(["div class","iframe"]),a.content=t.turndown(a.content),a.raise_patch(e)}}}))}set_listeners(){var e=this;$("body").on("click",".copy-link",function(){frappe.utils.copy_to_clipboard($(this).attr("data-link"))}),$("body").on("click",".delete-button",function(){frappe.confirm(`Are you sure you want to delete the file "${$(this).attr("data-name")}"`,()=>{e.attachments.forEach((a,i,t)=>{a.file_name==$(this).attr("data-name")&&t.splice(i,1)}),$(".wiki-attachment").empty().append(e.build_attachment_table()),$(".attachment-controls").find(".number").text(e.attachments.length)})})}create_comment_box(){this.comment_box=frappe.ui.form.make_control({parent:$(".comment-box"),df:{fieldname:"new_comment",fieldtype:"Comment"},enable_mentions:!1,render_input:!0,only_input:!0,on_submit:e=>{this.add_comment_to_patch(e)}})}add_comment_to_patch(e){strip_html(e).trim()!=""&&(this.comment_box.disable(),frappe.call({method:"wiki.wiki.doctype.wiki_page_patch.wiki_page_patch.add_comment_to_patch",args:{reference_name:$('[name="wiki_page_patch"]').val(),content:e,comment_email:frappe.session.user,comment_by:frappe.session.user_fullname},callback:a=>{e=a.message,this.display_new_comment(e,this.comment_box)},always:()=>{this.comment_box.enable()}}))}display_new_comment(e,a){if(e){a.set_value("");let i=this.get_comment_html(e.owner,e.creation,e.timepassed,e.content);$(".timeline-items").prepend(i)}}get_comment_html(e,a,i,t){return $(`
			<div class="timeline-item">
				<div class="timeline-badge">
					<svg class="icon icon-md">
						<use href="#icon-small-message"></use>
					</svg>
				</div>
				<div class="timeline-content frappe-card">
					<div class="timeline-message-box">
						<span class="flex justify-between">
							<span class="text-color flex">
								<span>
									${e}
									<span class="text-muted margin-left">
										<span class="frappe-timestamp "
											data-timestamp="${a}"
											title="${a}">${i}</span>
									</span>
								</span>
							</span>
						</span>
						<div class="content">
							${t}
						</div>
					</div>
				</div>
			</div>
		`)}make_title_editable(){let e=$(".edit-title>span"),a=$(".edit-title>i"),i=$(".edit-title>input");a.click(()=>{e.addClass("hide"),a.addClass("hide"),i.removeClass("hide"),i.val(e.text()),i.focus()}),i.focusout(()=>{e.removeClass("hide"),a.removeClass("hide"),i.addClass("hide"),e.text(i.val())}),i.on("change",t=>{$(".doc-sidebar .sidebar-items a.active").text(i.val())})}approve_wiki_page(){frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.approve",args:{wiki_page_patch:$('[name="wiki_page_patch"]').val()},callback:()=>{frappe.msgprint({message:"The Change has been approved.",indicator:"green",title:"Approved"}),window.location.href="/"+$('[name="wiki_page"]').val()},freeze:!0})}render_sidebar_diff(){let e=$(".sidebar-diff"),a=$('[name="new_sidebar_items"]').val(),i=a&&JSON.parse(a);e.empty();for(let t in i)for(let s in i[t]){let l=("."+t).replaceAll("/","\\/"),d=e.find(l);d.length||(d=$(".sidebar-diff")),i[t][s].type=="Wiki Sidebar"?$(d).append("<li>"+i[t][s].title+"</li><ul class="+i[t][s].group_name+"></ul>"):$(d).append("<li class="+i[t][s].group_name+">"+i[t][s].title+"</li>")}}};window.Wiki=class{activate_sidebars(){$(".sidebar-item").each(function(a){let i="active",t=window.location.pathname;t.indexOf("#")!==-1&&(t=t.slice(0,t.indexOf("#"))),$(this).data("route")==t&&($(this).addClass(i),$(this).find("a").addClass(i))});let e=$(".sidebar-item.active");e.length>0&&e.get(1).scrollIntoView(!0,{behavior:"smooth",block:"nearest"})}toggle_sidebar(e){$(e.currentTarget).parent().children("ul").toggleClass("hidden"),$(e.currentTarget).find(".drop-icon").toggleClass("hidden"),$(e.currentTarget).find(".drop-left").toggleClass("hidden"),e.stopPropagation()}set_active_sidebar(){$(".doc-sidebar,.web-sidebar").on("click",".collapsible",this.toggle_sidebar),$(".sidebar-group").children("ul").addClass("hidden"),$(".sidebar-item.active").parents(" .web-sidebar .sidebar-group>ul").removeClass("hidden");let e=$(".sidebar-item.active").parents(".web-sidebar .sidebar-group");e.each(function(){$(this).children(".collapsible").find(".drop-left").addClass("hidden")}),e.each(function(){$(this).children(".collapsible").find(".drop-icon").removeClass("hidden")})}scrolltotop(){$("html,body").animate({scrollTop:0},0)}};window.EditWiki=class extends Wiki{constructor(){super();frappe.provide("frappe.ui.keys"),$("document").ready(()=>{frappe.call("wiki.wiki.doctype.wiki_page.wiki_page.get_sidebar_for_page",{wiki_page:$('[name="wiki_page"]').val()}).then(e=>{$(".doc-sidebar").empty().append(e.message),this.activate_sidebars(),this.set_active_sidebar(),this.set_empty_ul(),this.set_sortable(),this.set_add_item(),this.scrolltotop()})})}activate_sidebars(){$(".sidebar-item").each(function(a){let i="active",t=window.location.pathname;t.indexOf("#")!==-1&&(t=t.slice(0,t.indexOf("#"))),t.split("/").slice(0,-1).join("/")==$(this).data("route")&&($('[name="new"]').first().val()?$(`
					<li class="sidebar-item active" data-type="Wiki Page" data-name="new-wiki-page" data-new=1>
						<div><div>
							<a href="#"  class ='active'>New Wiki Page</a>
						</div></div>
					</li>
				`).insertAfter($(this)):($(this).addClass(i),$(this).find("a").addClass(i)))});let e=$(".sidebar-item.active");e.length>0&&e.get(0).scrollIntoView(!0,{behavior:"smooth",block:"nearest"})}set_empty_ul(){$(".collapsible").each(function(){$(this).parent().find("ul").length==0&&$(this).parent().append($('<ul class="list-unstyled hidden" style="min-height:20px;"> </ul'))})}set_sortable(){$(".web-sidebar ul").each(function(){new Sortable(this,{group:{name:"qux",put:["qux"],pull:["qux"]}})})}set_add_item(){$(`<div class="text-muted add-sidebar-item small">+ Add Item</div>
			<div class="text-muted small mt-3"><i>Drag items to re-order</i></div>`).appendTo($(".web-sidebar"));var e=this;$(".add-sidebar-item").click(function(){var a=e.get_add_new_item_dialog_fields(),i=new frappe.ui.Dialog({title:"Add to sidebar",fields:a,primary_action:function(t){t.type=="Add Wiki Page"?e.add_wiki_page(t):t.type=="Group"?e.add_wiki_sidebar(t):t.type=="Page"&&e.add_wiki_sidebar_page(t),i.hide()}});i.show()})}get_add_new_item_dialog_fields(){return[{fieldname:"type",label:"Do you want to add a page or group?",fieldtype:"Select",options:["Page","Group"]},{fieldname:"wiki_page",label:"Wiki Page",fieldtype:"Link",options:"Wiki Page",depends_on:"eval: doc.type=='Page'",mandatory_depends_on:"eval: doc.type=='Page'"},{fieldname:"route",label:"Route",fieldtype:"Data",depends_on:"eval: doc.type=='Group'",mandatory_depends_on:"eval: doc.type=='Group'"},{fieldname:"title",label:"Title",fieldtype:"Data",depends_on:"eval: doc.type=='Group'",mandatory_depends_on:"eval: doc.type=='Group'"}]}add_wiki_page(e){var a=this;frappe.call({method:"frappe.client.get_value",args:{doctype:"Wiki Page",fieldname:"title",filters:e.wiki_page},callback:function(i){a.get_new_page_html(i,e).appendTo($(".doc-sidebar .sidebar-items").children(".list-unstyled").not(".hidden").first())}})}get_new_page_html(e,a){return $(`
		<li class="sidebar-item" data-type="Wiki Page"
			data-name="${a.wiki_page}" data-new=1 >
			<div>
				<div>
					<a href="#" class="green" >
							${e.message.title}
					</a>
				</div>
			</div>
		</li>
		`)}add_wiki_sidebar(e){this.get_wiki_sidebar_html(e).appendTo($(".doc-sidebar .sidebar-items").children(".list-unstyled").not(".hidden").first()),$(".web-sidebar ul").each(function(){new Sortable(this,{group:{name:"qux",put:["qux"],pull:["qux"]}})})}add_wiki_sidebar_page(e){var a=this;frappe.call({method:"frappe.client.get",args:{doctype:"Wiki Page",name:e.wiki_page},callback:function(i){a.get_wiki_sidebar_html(i.message).appendTo($(".doc-sidebar .sidebar-items").children(".list-unstyled").not(".hidden").first()),$(".web-sidebar ul").each(function(){new Sortable(this,{group:{name:"qux",put:["qux"],pull:["qux"]}})})}})}get_wiki_sidebar_html(e){return $(`
			<li class="sidebar-group" data-type="Wiki Sidebar"
				data-name="new-sidebar" data-group-name="${e.route}"
				data-new=1 data-title="${e.title}" draggable="false">

				<div class="collapsible">
					<span class="drop-icon hidden">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none"
								xmlns="http://www.w3.org/2000/svg">
								<path d="M8 10L12 14L16 10" stroke="#4C5A67"
								stroke-miterlimit="10" stroke-linecap="round"
								stroke-linejoin="round"></path>
							</svg>
					</span>

					<span class="drop-left">
							<svg width="24" height="24" viewBox="0 0 24 24"
								fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M10 16L14 12L10 8" stroke="#4C5A67"
								stroke-linecap="round" stroke-linejoin="round"></path>
							</svg>
					</span>
					<span class="h6">${e.title}</span>
					</div>
					<ul class="list-unstyled hidden" style="min-height:20px;"> </ul>
			</li>
			`)}};window.RenderWiki=class extends Wiki{constructor(e){super();$("document").ready(()=>{window.location.pathname!="/revisions"&&window.location.pathname!="/compare"&&(this.activate_sidebars(),this.set_active_sidebar(),this.set_nav_buttons(),this.set_toc_highlighter(),this.scrolltotop())})}set_toc_highlighter(){$(document).ready(function(){$(window).scroll(function(){s().not(".no-underline").hasClass("active")||($(".page-toc a").removeClass("active"),s().addClass("active"))})});function e(l){return $('[href="'+l+'"]')}function a(l){return $("[id="+l.substr(1)+"]")}var i=null;function t(){return i||(i=$(".page-toc a").map(function(){return $(this).attr("href")})),i}function s(){var l=window.pageYOffset,d=null;return t().each(function(){var r=a(this).position().top;if(r<l+window.innerHeight*.23){d=this;return}}),e(d)}}set_nav_buttons(){var e=-1;$(".sidebar-column").find("a").each(function(a){$(this).attr("class")&&$(this).attr("class").split(/\s+/)[0]==="active"&&(e=a)}),e>0?($(".btn.left")[0].href=$(".sidebar-column").find("a")[e-1].href,$(".btn.left")[0].innerHTML="\u2190"+$(".sidebar-column").find("a")[e-1].innerHTML):$(".btn.left").hide(),e>=0&&e<$(".sidebar-column").find("a").length-1?($(".btn.right")[0].href=$(".sidebar-column").find("a")[e+1].href,$(".btn.right")[0].innerHTML=$(".sidebar-column").find("a")[e+1].innerHTML+"\u2192"):$(".btn.right").hide()}};window.EditWikiAr=class extends Wiki{constructor(){super();frappe.provide("frappe.ui.keys"),$("document").ready(()=>{frappe.call("wiki.wiki.doctype.wiki_page.wiki_page.get_sidebar_for_page",{wiki_page:$('[name="wiki_page"]').val()}).then(e=>{$(".doc-sidebar").empty().append(e.message),this.activate_sidebars(),this.set_active_sidebar(),this.set_empty_ul(),this.set_sortable(),this.set_add_item(),this.scrolltotop()})})}activate_sidebars(){$(".sidebar-item").each(function(a){let i="active",t=window.location.pathname;t.indexOf("#")!==-1&&(t=t.slice(0,t.indexOf("#"))),t.split("/").slice(0,-1).join("/")==$(this).data("route")&&($('[name="new"]').first().val()?$(`
					<li class="sidebar-item active" data-type="Wiki Page" data-name="new-wiki-page" data-new=1>
						<div><div>
							<a href="#"  class ='active'>\u0635\u0641\u062D\u0629 \u0648\u064A\u0643\u064A \u062C\u062F\u064A\u062F\u0629</a>
						</div></div>
					</li>
				`).insertAfter($(this)):($(this).addClass(i),$(this).find("a").addClass(i)))});let e=$(".sidebar-item.active");e.length>0&&e.get(0).scrollIntoView(!0,{behavior:"smooth",block:"nearest"})}set_empty_ul(){$(".collapsible").each(function(){$(this).parent().find("ul").length==0&&$(this).parent().append($('<ul class="list-unstyled hidden" style="min-height:20px;"> </ul'))})}set_sortable(){$(".web-sidebar ul").each(function(){new Sortable(this,{group:{name:"qux",put:["qux"],pull:["qux"]}})})}set_add_item(){$(`<div class="text-muted add-sidebar-item small">+ \u0627\u0636\u0627\u0641\u0629 \u0639\u0646\u0635\u0631 </div>
			<div class="text-muted small mt-3"><i>\u0627\u0633\u062D\u0628 \u0627\u0644\u0639\u0646\u0627\u0635\u0631 \u0644\u0625\u0639\u0627\u062F\u0629 \u062A\u0631\u062A\u064A\u0628\u0647\u0627 </i></div>`).appendTo($(".web-sidebar"));var e=this;$(".add-sidebar-item").click(function(){var a=e.get_add_new_item_dialog_fields(),i=new frappe.ui.Dialog({title:"Add to sidebar",fields:a,primary_action:function(t){t.type=="Add Wiki Page"?e.add_wiki_page(t):t.type=="Group"?e.add_wiki_sidebar(t):t.type=="Page"&&e.add_wiki_sidebar_page(t),i.hide()}});i.show()})}get_add_new_item_dialog_fields(){return[{fieldname:"type",label:"Do you want to add a page or group?",fieldtype:"Select",options:["Page","Group"]},{fieldname:"wiki_page",label:"Wiki Page",fieldtype:"Link",options:"Wiki Page",depends_on:"eval: doc.type=='Page'",mandatory_depends_on:"eval: doc.type=='Page'"},{fieldname:"route",label:"Route",fieldtype:"Data",depends_on:"eval: doc.type=='Group'",mandatory_depends_on:"eval: doc.type=='Group'"},{fieldname:"title",label:"Title",fieldtype:"Data",depends_on:"eval: doc.type=='Group'",mandatory_depends_on:"eval: doc.type=='Group'"}]}add_wiki_page(e){var a=this;frappe.call({method:"frappe.client.get_value",args:{doctype:"Wiki Page",fieldname:"title",filters:e.wiki_page},callback:function(i){a.get_new_page_html(i,e).appendTo($(".doc-sidebar .sidebar-items").children(".list-unstyled").not(".hidden").first())}})}get_new_page_html(e,a){return $(`
		<li class="sidebar-item" data-type="Wiki Page"
			data-name="${a.wiki_page}" data-new=1 >
			<div>
				<div>
					<a href="#" class="green" >
							${e.message.title}
					</a>
				</div>
			</div>
		</li>
		`)}add_wiki_sidebar(e){this.get_wiki_sidebar_html(e).appendTo($(".doc-sidebar .sidebar-items").children(".list-unstyled").not(".hidden").first()),$(".web-sidebar ul").each(function(){new Sortable(this,{group:{name:"qux",put:["qux"],pull:["qux"]}})})}add_wiki_sidebar_page(e){var a=this;frappe.call({method:"frappe.client.get",args:{doctype:"Wiki Page",name:e.wiki_page},callback:function(i){a.get_wiki_sidebar_html(i.message).appendTo($(".doc-sidebar .sidebar-items").children(".list-unstyled").not(".hidden").first()),$(".web-sidebar ul").each(function(){new Sortable(this,{group:{name:"qux",put:["qux"],pull:["qux"]}})})}})}get_wiki_sidebar_html(e){return $(`
			<li class="sidebar-group" data-type="Wiki Sidebar"
				data-name="new-sidebar" data-group-name="${e.route}"
				data-new=1 data-title="${e.title}" draggable="false">

				<div class="collapsible">
					<span class="drop-icon hidden">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none"
								xmlns="http://www.w3.org/2000/svg">
								<path d="M8 10L12 14L16 10" stroke="#4C5A67"
								stroke-miterlimit="10" stroke-linecap="round"
								stroke-linejoin="round"></path>
							</svg>
					</span>

					<span class="drop-left">
							<svg width="24" height="24" viewBox="0 0 24 24"
								fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M10 16L14 12L10 8" stroke="#4C5A67"
								stroke-linecap="round" stroke-linejoin="round"></path>
							</svg>
					</span>
					<span class="h6">${e.title}</span>
					</div>
					<ul class="list-unstyled hidden" style="min-height:20px;"> </ul>
			</li>
			`)}};window.EditAssetAr=class{constructor(){this.make_code_field_group(),this.add_attachment_popover(),this.set_code_editor_height(),this.render_preview(),this.add_attachment_handler(),this.set_listeners(),this.create_comment_box(),this.make_title_editable(),this.render_sidebar_diff()}make_code_field_group(){this.code_field_group=new frappe.ui.FieldGroup({fields:[{fieldname:"type",fieldtype:"Data",default:"Rich Text",options:"Rich Text"},{fieldtype:"Section Break"},{fieldname:"code_html",fieldtype:"Text Editor",default:$(".wiki-content-html").html(),depends_on:'eval:doc.type=="Rich Text"'}],body:$(".wiki-write").get(0)}),this.code_field_group.make(),$(".wiki-write .form-section:last").removeClass("empty-section")}get_attachment_controls_html(){return`
			<div class="attachment-controls">
				<div class="show-attachments" tabindex="-1" data-trigger="focus">
					${this.get_show_uploads_svg()}
					<span class="number">0</span> \u0627\u0644\u0645\u0631\u0641\u0642
				</div>
				<div class="add-attachment-wiki">
					<span class="btn">
						${this.get_upload_image_svg()}
						\u062A\u062D\u0645\u064A\u0644 \u0627\u0644\u0645\u0631\u0641\u0642
					</span>
				</div>
			</div>
		`}get_show_uploads_svg(){return`<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path d="M12.6004 6.68841L7.6414 11.5616C6.23259 12.946 3.8658 12.946 2.45699 11.5616C1.04819 10.1772
			1.04819 7.85132 2.45699 6.4669L6.85247 2.14749C7.86681 1.15071 9.44467 1.15071 10.459 2.14749C11.4733
			3.14428 11.4733 4.69483 10.459 5.69162L6.40165 9.62339C5.83813 10.1772 4.93649 10.1772 4.42932 9.62339C3.8658
			9.06962 3.8658 8.18359 4.42932 7.68519L7.81045 4.36257" stroke="#2D95F0" stroke-miterlimit="10" stroke-linecap="round"/>
		</svg>`}get_upload_image_svg(){return`<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path d="M8 14.5C11.5899 14.5 14.5 11.5899 14.5 8C14.5 4.41015 11.5899 1.5 8 1.5C4.41015 1.5 1.5 4.41015 1.5 8C1.5 11.5899
			 4.41015 14.5 8 14.5Z" stroke="#505A62" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
			<path d="M8 4.75V11.1351" stroke="#505A62" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
			<path d="M5.29102 7.45833L7.99935 4.75L10.7077 7.45833" stroke="#505A62" stroke-miterlimit="10" stroke-linecap="round"
			stroke-linejoin="round"/>
		</svg>`}add_attachment_popover(){$(".show-attachments").popover({placement:"bottom",content:()=>this.build_attachment_table(),html:!0})}build_attachment_table(){var e=$('<div class="wiki-attachment"></div>');e.empty();var a=$(this.get_attachment_table_header_html()).appendTo(e);if(!this.attachments||!this.attachments.length)return"No attachments uploaded";let i=t=>t.split("/").pop().split(".").slice(0,-1).join(".").replaceAll("_"," ").replaceAll("-"," ");return this.attachments.forEach(t=>{let s=$("<tr></tr>").appendTo(a.find("tbody"));$(`<td>${t.file_name}</td>`).appendTo(s),$(`<td>
			<a class="btn btn-default btn-xs btn-primary-light text-nowrap copy-link" data-link="![${i(t.file_url)}](${t.file_url})" data-name = "${t.file_name}" >
				Copy Link
			</a>
			</td>`).appendTo(s),$(`<td>

			<a class="btn btn-default btn-xs  center delete-button"  data-name = "${t.file_name}" >
			<svg class="icon icon-sm"><use xlink:href="#icon-delete"></use></svg>

			</a>
			</td>`).appendTo(s)}),e}get_attachment_table_header_html(){return`<table class="table  attachment-table" ">
			<tbody></tbody>
		</table>`}set_code_editor_height(){setTimeout(()=>{let e=this.code_field_group.get_field("code_md");e.expanded=!this.expanded,e.refresh_height(),e.toggle_label()},120)}raise_patch(e=!1){var a={};let i=$(".doc-sidebar .web-sidebar").get(0).dataset.name;a[i]=[];let t=$($(".doc-sidebar .web-sidebar").get(0)).children(".sidebar-items").children("ul").not(".hidden").children("li");t.each(n=>{!t[n].dataset.name||a[i].push({name:t[n].dataset.name,type:t[n].dataset.type,new:t[n].dataset.new,title:t[n].dataset.title,group_name:t[n].dataset.groupName})}),$('.doc-sidebar [data-type="Wiki Sidebar"]').each(function(){let n=$(this).get(0).dataset.groupName;a[n]=[];let o=$(this).children("ul").children("li");o.each(p=>{!o[p].dataset.name||a[n].push({name:o[p].dataset.name,type:o[p].dataset.type,new:o[p].dataset.new,title:o[p].dataset.title,group_name:o[p].dataset.groupName})})});var s=this,l=[];let d=$(".edit-title span").text();l.push({fieldname:"edit_message",fieldtype:"Text",label:"Message",default:$('[name="new"]').val()?`Add new page: ${d}`:`${d} \u062A\u0645 \u062A\u062D\u0631\u064A\u0631\u0647`,mandatory:1},{fieldname:"sidebar_edited",fieldtype:"Check",label:"\u0644\u0642\u062F \u0642\u0645\u062A \u0628\u062A\u062D\u062F\u064A\u062B \u0627\u0644\u0634\u0631\u064A\u0637 \u0627\u0644\u062C\u0627\u0646\u0628\u064A",default:$('[name="new"]').val()?1:0});let r=new frappe.ui.Dialog({fields:l,title:__("\u0631\u062C\u0649 \u0648\u0635\u0641 \u0627\u0644\u062A\u063A\u064A\u064A\u0631\u0627\u062A \u0627\u0644\u062E\u0627\u0635\u0629 \u0628\u0643"),primary_action_label:__("\u0623\u0631\u0633\u0644 \u0627\u0644\u062A\u063A\u064A\u064A\u0631\u0627\u062A"),primary_action:function(){frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.update",args:{name:$('[name="wiki_page"]').val(),wiki_page_patch:$('[name="wiki_page_patch"]').val(),message:this.get_value("edit_message"),sidebar_edited:this.get_value("sidebar_edited"),content:s.content,type:s.code_field_group.get_value("type"),attachments:s.attachments,new:$('[name="new"]').val(),title:$(".edit-title span").text(),new_sidebar:$(".doc-sidebar").get(0).innerHTML,new_sidebar_items:a,draft:e||null},callback:n=>{!n.message.approved&&n.message.route=="contributions"?frappe.msgprint({message:"\u062A\u0645 \u0625\u0646\u0634\u0627\u0621 \u0637\u0644\u0628 \u062A\u063A\u064A\u064A\u0631. \u064A\u0645\u0643\u0646\u0643 \u062A\u062A\u0628\u0639 \u0637\u0644\u0628\u0627\u062A\u0643 \u0639\u0644\u0649 \u0635\u0641\u062D\u0629 \u0627\u0644\u0645\u0633\u0627\u0647\u0645\u0627\u062A",indicator:"green",title:"\u062A\u0645 \u0625\u0646\u0634\u0627\u0621 \u0637\u0644\u0628 \u0627\u0644\u062A\u063A\u064A\u064A\u0631",alert:1}):!n.message.approved&&n.message.route=="drafts"&&frappe.msgprint({message:"\u062A\u0645 \u062D\u0641\u0638 \u0627\u0644\u0645\u0633\u0648\u062F\u0629",indicator:"green",title:"\u062A\u0645 \u0625\u0646\u0634\u0627\u0621 \u0637\u0644\u0628 \u0627\u0644\u062A\u063A\u064A\u064A\u0631",alert:1}),window.location.href="/"+n.message.route},freeze:!0}),r.hide(),$("#freeze").addClass("show")}});r.show()}render_preview(){$('a[data-toggle="tab"]').on("click",e=>{let a=$(e.target);if(a.prop("id")==="preview-tab"||a.prop("id")==="diff-tab"){let t=$(".wiki-preview"),s=$(".wiki-diff"),l=this.code_field_group.get_value("type"),d="";if(l=="Markdown")d=this.code_field_group.get_value("code_md");else{d=this.code_field_group.get_value("code_html");var i=new TurndownService;i=i.keep(["div class","iframe"]),d=i.turndown(d)}if(!d){this.set_empty_message(t,s);return}this.set_loading_message(t,s),frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.preview",args:{content:d,type:l,path:this.route,name:$('[name="wiki_page"]').val(),attachments:this.attachments,new:$('[name="new"]').val()},callback:r=>{if(r.message&&(t.html(r.message.html),!$('[name="new"]').val())){let n='<div class="text-muted center"> \u0644\u0645 \u064A\u062A\u0645 \u0625\u062C\u0631\u0627\u0621 \u0623\u064A \u062A\u063A\u064A\u064A\u0631\u0627\u062A</div>',o=$(r.message.diff).find(".insert, .delete").length?r.message.diff:n;s.html(o)}}})}})}set_empty_message(e,a){e.html("<div>\u0627\u0644\u0631\u062C\u0627\u0621 \u0625\u0636\u0627\u0641\u0629 \u0628\u0639\u0636 \u0627\u0644\u0643\u0648</div>"),a.html("<div>\u0627\u0644\u0631\u062C\u0627\u0621 \u0625\u0636\u0627\u0641\u0629 \u0628\u0639\u0636 \u0627\u0644\u0643\u0648</div>")}set_loading_message(e,a){e.html("...\u0645\u0639\u0627\u064A\u0646\u0629 \u0627\u0644\u062A\u062D\u0645\u064A\u0644"),a.html("...\u0641\u0631\u0642 \u0627\u0644\u062A\u062D\u0645\u064A\u0644")}add_attachment_handler(){var e=this;$(".add-attachment-wiki").click(function(){e.new_attachment()}),$(".submit-wiki-page").click(function(){e.get_markdown()}),$(".draft-wiki-page").click(function(){e.get_markdown(!0)})}new_attachment(){this.dialog&&this.dialog.$wrapper.remove(),new frappe.ui.FileUploader({folder:"Home/Attachments",on_success:e=>{this.attachments||(this.attachments=[]),this.save_paths||(this.save_paths={}),this.attachments.push(e),$(".wiki-attachment").empty().append(this.build_attachment_table()),$(".attachment-controls").find(".number").text(this.attachments.length)}})}get_markdown(e=!1){var a=this;a.code_field_group.get_value("type")=="Markdown"?(this.content=a.code_field_group.get_value("code_md"),this.raise_patch(e)):(this.content=this.code_field_group.get_value("code_html"),frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.extract_images_from_html",args:{content:this.content},callback:i=>{if(i.message){a.content=i.message;var t=new TurndownService;t=t.keep(["div class","iframe"]),a.content=t.turndown(a.content),a.raise_patch(e)}}}))}set_listeners(){var e=this;$("body").on("click",".copy-link",function(){frappe.utils.copy_to_clipboard($(this).attr("data-link"))}),$("body").on("click",".delete-button",function(){frappe.confirm(`\u0647\u0644 \u0623\u0646\u062A \u0645\u062A\u0623\u0643\u062F \u0623\u0646\u0643 \u062A\u0631\u064A\u062F \u062D\u0630\u0641 \u0627\u0644\u0645\u0644\u0641 "${$(this).attr("data-name")}"`,()=>{e.attachments.forEach((a,i,t)=>{a.file_name==$(this).attr("data-name")&&t.splice(i,1)}),$(".wiki-attachment").empty().append(e.build_attachment_table()),$(".attachment-controls").find(".number").text(e.attachments.length)})})}create_comment_box(){this.comment_box=frappe.ui.form.make_control({parent:$(".comment-box"),df:{fieldname:"new_comment",fieldtype:"Comment"},enable_mentions:!1,render_input:!0,only_input:!0,on_submit:e=>{this.add_comment_to_patch(e)}})}add_comment_to_patch(e){strip_html(e).trim()!=""&&(this.comment_box.disable(),frappe.call({method:"wiki.wiki.doctype.wiki_page_patch.wiki_page_patch.add_comment_to_patch",args:{reference_name:$('[name="wiki_page_patch"]').val(),content:e,comment_email:frappe.session.user,comment_by:frappe.session.user_fullname},callback:a=>{e=a.message,this.display_new_comment(e,this.comment_box)},always:()=>{this.comment_box.enable()}}))}display_new_comment(e,a){if(e){a.set_value("");let i=this.get_comment_html(e.owner,e.creation,e.timepassed,e.content);$(".timeline-items").prepend(i)}}get_comment_html(e,a,i,t){return $(`
			<div class="timeline-item">
				<div class="timeline-badge">
					<svg class="icon icon-md">
						<use href="#icon-small-message"></use>
					</svg>
				</div>
				<div class="timeline-content frappe-card">
					<div class="timeline-message-box">
						<span class="flex justify-between">
							<span class="text-color flex">
								<span>
									${e}
									<span class="text-muted margin-left">
										<span class="frappe-timestamp "
											data-timestamp="${a}"
											title="${a}">${i}</span>
									</span>
								</span>
							</span>
						</span>
						<div class="content">
							${t}
						</div>
					</div>
				</div>
			</div>
		`)}make_title_editable(){let e=$(".edit-title>span"),a=$(".edit-title>i"),i=$(".edit-title>input");a.click(()=>{e.addClass("hide"),a.addClass("hide"),i.removeClass("hide"),i.val(e.text()),i.focus()}),i.focusout(()=>{e.removeClass("hide"),a.removeClass("hide"),i.addClass("hide"),e.text(i.val())}),i.on("change",t=>{$(".doc-sidebar .sidebar-items a.active").text(i.val())})}approve_wiki_page(){frappe.call({method:"wiki.wiki.doctype.wiki_page.wiki_page.approve",args:{wiki_page_patch:$('[name="wiki_page_patch"]').val()},callback:()=>{frappe.msgprint({message:"The Change has been approved.",indicator:"green",title:"Approved"}),window.location.href="/"+$('[name="wiki_page"]').val()},freeze:!0})}render_sidebar_diff(){let e=$(".sidebar-diff"),a=$('[name="new_sidebar_items"]').val(),i=a&&JSON.parse(a);e.empty();for(let t in i)for(let s in i[t]){let l=("."+t).replaceAll("/","\\/"),d=e.find(l);d.length||(d=$(".sidebar-diff")),i[t][s].type=="Wiki Sidebar"?$(d).append("<li>"+i[t][s].title+"</li><ul class="+i[t][s].group_name+"></ul>"):$(d).append("<li class="+i[t][s].group_name+">"+i[t][s].title+"</li>")}}};})();
//# sourceMappingURL=wiki_override.bundle.Y26C7RGI.js.map
