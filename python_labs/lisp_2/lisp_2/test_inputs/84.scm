(define some_list (list -1 2 -3 4 -5 6 -7 8))
(reduce + (map (lambda (i) (* i i)) (filter (lambda (i) (< i 0)) some_list)) 1)
some_list
(reduce + (map (lambda (i) (* i i)) (filter (lambda (i) (< i 0)) (list -3 -13 20))) 93)
(reduce + (map (lambda (i) (* i i)) (filter (lambda (i) (< i 0)) (list 1 2 3 4))) 82)
(reduce + (map (lambda (i) (* i i)) (filter (lambda (i) (< i 0)) (list))) 37)
(reduce append (map (lambda (i) (append (list 2) i)) (filter (lambda (i) (< (length i) 4)) (list (list) (list 9 8 7 6 5) (list 1 2 3) (list 34)))) (list))
