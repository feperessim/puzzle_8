(use-modules (srfi srfi-1)
             (srfi srfi-13)
	     (ice-9 hash-table))

(define nil '())

;; To use strings as keys we must defiine
;; the procedures bellow
;; Example extracted from:
;; https://www.gnu.org/software/guile/manual/html_node/Hash-Table-Reference.html#Hash-Table-Reference
(define (my-hash str size)
  (remainder (string-hash-ci str) size))

(define (my-assoc str alist)
  (find (lambda (pair) (string-ci=? str (car pair))) alist))

(define (hash-set! table key val)
  (hashx-set! my-hash my-assoc table key val))

(define (hash-ref table key)
  (hashx-ref my-hash my-assoc table key))

;; displays the board on screen
(define (display-board board)
  (define (show rest-of-board index)
    (cond ((null? rest-of-board)
	   (newline))
	  ((= (remainder index 3) 0)
	   (display " ")
	   (display (car rest-of-board))
	   (display " ")
	   (newline)
	   (show (cdr rest-of-board)
		 (+ 1 index)))
	  (else
	   (display " ")
	   (display (car rest-of-board))
	   (display " ")
	   (show (cdr rest-of-board)
		 (+ 1 index)))))
  (show board 1))

;; Lookup the index of an element from a list
;; returns -1 in case the element is not on the
;; list.
(define (find-index lst element)
  (define (loop lst index)
    (cond ((null? lst) -1)
	  ((string=? (car lst) element) index)
	  (else
	   (loop (cdr lst) (+ 1 index)))))
  (loop lst 0))


(define (move-left board index-empty-cell)
  (cond
   ((or
    (and
     (> index-empty-cell 0)
     (< index-empty-cell 3))
    (and
     (> index-empty-cell 3)
     (< index-empty-cell 6))
    (and
     (> index-empty-cell 6)
     (< index-empty-cell 9)))
    (let
	((to-swap
	  (list-ref
	   board (- index-empty-cell 1))))
      (map
       (λ (element)
	 (cond
	  ((string=? element to-swap)
	   empty-cell)
	  ((string=? element empty-cell)
	   to-swap)
	  (else element)))
       board)))
   (else nil)))

(define (move-right board index-empty-cell)
  (cond
   ((or
    (and
     (>= index-empty-cell 0)
     (< index-empty-cell 2))
    (and
     (>= index-empty-cell 3)
     (< index-empty-cell 5))
    (and
     (>= index-empty-cell 6)
     (< index-empty-cell 8)))
    (let
	((to-swap
	  (list-ref
	   board (+ index-empty-cell 1))))
      (map
       (λ (element)
	 (cond
	  ((string=? element to-swap)
	   empty-cell)
	  ((string=? element empty-cell)
	   to-swap)
	  (else element)))
       board)))
   (else nil)))

(define (move-up board index-empty-cell)
  (cond
   ((>= index-empty-cell 3)
    (let
	((to-swap
	  (list-ref
	   board (- index-empty-cell 3))))
      (map
       (λ (element)
	 (cond
	  ((string=? element to-swap)
	   empty-cell)
	  ((string=? element empty-cell)
	   to-swap)
	  (else element)))
       board)))
   (else nil)))

(define (move-down board index-empty-cell)
  (cond
   ((<= index-empty-cell 5)
    (let
	((to-swap
	  (list-ref
	   board (+ index-empty-cell 3))))
      (map
       (λ (element)
	 (cond
	  ((string=? element to-swap)
	   empty-cell)
	  ((string=? element empty-cell)
	   to-swap)
	  (else element)))
       board)))
   (else nil)))

(define (generate-adjacency-list board)
  (let
      ((index-empty-cell
	(find-index
	 board
	 empty-cell)))
    (filter
     (λ (lst) (not (null? lst)))
     (list
      (move-left board index-empty-cell)
      (move-right board index-empty-cell)
      (move-up board index-empty-cell)
      (move-down board index-empty-cell)))))

(define (for-each p l)
  (cond ((null? l) #t)
        (else
         (p (car l))
         (for-each p (cdr l)))))

(define empty-cell "0")
(define boards (make-hash-table))
(define path (make-hash-table))

(define root-board (list "2" "6" "0" "5" "7" "3" "8" "1" "4"))
(define goal-board (list "1" "2" "3" "4" "5" "6" "7" "8" "0"))

(hash-set! path
	   (string-join root-board)
	   '())

(display-board root-board)
(display-board goal-board)

(define (bfs root-board goal-board)
  (define (horizontal-walk frontier)
    (cond
     ((null? frontier)
      (list path
	    root-board))
     ((string=?
      (string-join (car frontier) " ")
      (string-join goal-board " "))
      (list
       path
       (car frontier)))
     (else
      (let
	  ((parent
	    (car frontier))
	   (children
	    (filter
	     (λ (board)
	       (not
		(hash-ref
		 path
		 (string-join board " "))))
	     (generate-adjacency-list (car frontier)))))
	(for-each
	 (λ (board)
	   (hash-set!
	    path
	    (string-join board " ")
	    (string-join parent " ")))
	 children)
	(horizontal-walk
	 (append
	  (cdr frontier)
	  children))))))
  (horizontal-walk
   (list root-board)))

(define (reconstruct-path path board boards)
  (let ((new_board (hash-ref
		    path
		    (string-join board))))
    (if (null? new_board)
	boards
	(reconstruct-path
	 path
	 (string-split new_board #\space)
	 (append
	  boards
	  (list
	   (string-split new_board #\space)))))))
	
	     
(define (show-boards boards)
  (for-each
   (λ (board) (display-board board))
   boards))

(bfs root-board goal-board)

(define boards
  (reconstruct-path
   path
   (list "1" "2" "3" "4" "5" "6" "7" "8" "0")
   (list
    (list "1" "2" "3" "4" "5" "6" "7" "8" "0"))))

(show-boards boards)
