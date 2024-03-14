// Copyright (c) 2024, mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Zk Settings", {
	refresh(frm) {



	},
	filter_logs:function(frm){
			// frappe.msgprint('hello')
			frappe.call({
				method:"zk_api.api.filter_device_logs",
				args:{
					"start_d":frm.doc.start_date,
					"end_d":frm.doc.end_date
				},
				dotype:"Device Log",
				callback:function(r){
					console.log('hello')
					console.log(r)
				}
			})
		}
});
