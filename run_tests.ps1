$test_filename=$args[0]
if($args.count -eq 0){
    python -m unittest  discover -v --catch gbpacman/tests
}else{
        $test_filepath="gbpacman/tests/test_"+$test_filename+".py"
        $message="Running test for "+$test_filepath
        echo $message
        python -m unittest  $test_filepath
    }
