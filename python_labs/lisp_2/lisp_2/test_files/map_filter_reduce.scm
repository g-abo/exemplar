(begin
  (define  (map function lst)
    (if  (equal? (length lst) 0)
        (list)  
               (cons ( function (car lst))  (map function (cdr lst)))))

        (define (filter function lst)
           (if (equal? (length lst) 0)
        (list)  
        (if (function (car lst))
            (cons (car lst) (filter  function (cdr lst)))  
            (filter function (cdr lst)))))

    (define  (reduce function lst  initval)
               (if (equal? (length lst) 0)
      initval  
      (reduce  function (cdr lst) (function initval (car lst))))))
