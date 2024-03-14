// Copyright (c) 2024, mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Zk Settings", {
	
	filter_logs:function(frm){
			// frappe.msgprint('hello')
		if(!frm.doc.end_date && !frm.doc.start_date){
			frappe.msgprint('You must enetr start and End Date')
		}
		else{
			frm.clear_table('device_logs')


			frappe.call({
				method:"zk_api.api.filter_device_logs",
				args:{
					"start_d":frm.doc.start_date,
					"end_d":frm.doc.end_date
				},
				dotype:"Device Log",
				callback:function(r){
					console.log('hello')
					// console.log(r.message)
					data=r.message
					console.log(data)
					data.forEach((item) => {
						frm.add_child("device_logs",{
						

							enroll_no:item["enroll_no"],
							time:item['time'],
							date:item['date'],
							type:item['type']
						})

					})
					frm.refresh_field('device_logs')

				}
			})
			
		
		}
		},

		// get_logs:function(frm){
		// 	frappe.show_progress(__("Loading Device Logs"),0.5)
		// 	frappe.call({
		// 		method:"zk_api.api.get_log",
		// 		callback:function(r){
		// 			if (r.message){

		// 			}
		// 			  frappe.hide_progress();

		// 		},
		// 		error: function(err) {
        //     frappe.hide_progress();
        //     frappe.msgprint(__('Failed to load Device Logs. Please try again.'));
        //     console.error(err);
        // },
        //        always: function() {
        //        console.log("Always function called");
        //           frappe.hide_progress();
        //           }
		// 	})
		// }

		get_logs:function(frm){
    frappe.show_progress(__("Loading Device Logs"),0.5)
    frappe.call({
        method:"zk_api.api.get_log",
        callback:function(r){
            if (r.message){
                // handle the response here
            }
            frappe.hide_progress();
        },
        error: function(err) {
            frappe.msgprint(__('Failed to load Device Logs. Please try again.'));
            console.error(err);
            frappe.hide_progress();
        },
        always: function() {
            console.log("Always function called");
        }
    })
}




});
