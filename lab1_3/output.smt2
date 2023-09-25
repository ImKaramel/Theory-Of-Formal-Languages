(set-logic QF_NIA)
(define-fun arcMax2 ((x1 Int) (x2 Int)) Int (ite (> x1 x2) x1 x2))
(define-fun arcSum2 ((x1 Int) (x2 Int)) Int (ite (= x1 -1) x1 (ite (= x2 -1) x2 (+ x1 x2))))
(define-fun >> ((a Int) (b Int)) Bool (or (> a b) (and (= a -1) (= b -1))))
(define-fun arcMax3 ((x1 Int) (x2 Int) (x3 Int)) Int (ite (> x1 (arcMax2 x2 x3)) x1 (arcMax2 x2 x3)))
(define-fun arcMax4 ((x1 Int) (x2 Int) (x3 Int) (x4 Int)) Int (ite (> x1 (arcMax3 x2 x3 x4)) x1 (arcMax3 x2 x3 x4)))
(define-fun arcMax5 ((x1 Int) (x2 Int) (x3 Int) (x4 Int) (x5 Int)) Int (ite (> x1 (arcMax4 x2 x3 x4 x5)) x1 (arcMax4 x2 x3 x4 x5)))
(define-fun arcMax6 ((x1 Int) (x2 Int) (x3 Int) (x4 Int) (x5 Int) (x6 Int)) Int (ite (> x1 (arcMax5 x2 x3 x4 x5 x6)) x1 (arcMax5 x2 x3 x4 x5 x6)))
(define-fun arcMax7 ((x1 Int) (x2 Int) (x3 Int) (x4 Int) (x5 Int) (x6 Int) (x7 Int)) Int (ite (> x1 (arcMax6 x2 x3 x4 x5 x6 x7)) x1 (arcMax6 x2 x3 x4 x5 x6 x7)))
(define-fun arcSum3 ((x1 Int) (x2 Int) (x3 Int)) Int (ite (= x1 -1) x1 (ite (= (arcSum2 x2 x3) -1) (arcSum2 x2 x3) (+ x1 (arcSum2 x2 x3)))))
(declare-fun a11 () Int)
(declare-fun a21 () Int)
(declare-fun a31 () Int)
(declare-fun a41 () Int)
(declare-fun b11 () Int)
(declare-fun b21 () Int)
(declare-fun a12 () Int)
(declare-fun a22 () Int)
(declare-fun a32 () Int)
(declare-fun a42 () Int)
(declare-fun b12 () Int)
(declare-fun b22 () Int)
(declare-fun a13 () Int)
(declare-fun a23 () Int)
(declare-fun a33 () Int)
(declare-fun a43 () Int)
(declare-fun b13 () Int)
(declare-fun b23 () Int)
(assert (>> (arcMax4 (arcSum3 a11 a12 a12) (arcSum3 a31 a22 a12) (arcSum3 a11 a32 a22) (arcSum3 a31 a42 a22)) a13))
(assert (>> (arcMax4 (arcSum3 a21 a12 a12) (arcSum3 a41 a22 a12) (arcSum3 a21 a32 a22) (arcSum3 a41 a42 a22)) a23))
(assert (>> (arcMax4 (arcSum3 a11 a12 a32) (arcSum3 a31 a22 a32) (arcSum3 a11 a32 a42) (arcSum3 a31 a42 a42)) a33))
(assert (>> (arcMax4 (arcSum3 a21 a12 a32) (arcSum3 a41 a22 a32) (arcSum3 a21 a32 a42) (arcSum3 a41 a42 a42)) a43))
(assert (>> (arcMax7 (arcSum3 b11 a12 a12) (arcSum3 b21 a22 a12) (arcSum2 b12 a12) (arcSum3 b11 a32 a22) (arcSum3 b21 a42 a22) (arcSum2 b22 a22) b12) b13))
(assert (>> (arcMax7 (arcSum3 b11 a12 a32) (arcSum3 b21 a22 a32) (arcSum2 b12 a32) (arcSum3 b11 a32 a42) (arcSum3 b21 a42 a42) (arcSum2 b22 a42) b22) b23))
(assert (>> a13 a12))
(assert (>> a23 a22))
(assert (>> a33 a32))
(assert (>> a43 a42))
(assert (>> b13 b12))
(assert (>> b23 b22))
(assert (>= a11 0))
(assert (or (>= a21 0) (= a21 -1)))
(assert (or (>= a31 0) (= a31 -1)))
(assert (or (>= a41 0) (= a41 -1)))
(assert (>= b11 0))
(assert (or (>= b21 0) (= b21 -1)))
(assert (>= a12 0))
(assert (or (>= a22 0) (= a22 -1)))
(assert (or (>= a32 0) (= a32 -1)))
(assert (or (>= a42 0) (= a42 -1)))
(assert (>= b12 0))
(assert (or (>= b22 0) (= b22 -1)))
(assert (>= a13 0))
(assert (or (>= a23 0) (= a23 -1)))
(assert (or (>= a33 0) (= a33 -1)))
(assert (or (>= a43 0) (= a43 -1)))
(assert (>= b13 0))
(assert (or (>= b23 0) (= b23 -1)))
(check-sat)
(get-model)
