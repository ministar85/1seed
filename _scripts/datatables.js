 $(document).ready( function () {
    $('#table_id').DataTable( {
        colReorder: true,
        rowReorder: { update: true },
        // bProcessing: true,

        // bjQueryUI: true,

        //autoFill: true,

        // responsive: true,
        
        //grouping of the rows:
        //rowGroup: {
        //    dataSrc: '2'
        //},


        buttons: [
            'copy', 'excel', 'pdf'
        ]
    } );
} );