JsOsaDAS1.001.00bplist00�Vscript_�ObjC.import('stdlib');

function run(argv) {
	if (argv.length > 1) {
    	// Get major version number
    	var v = argv[1];

    	Application('Alfred ' + v).search(argv[0]);
	}
}                            �jscr  ��ޭ