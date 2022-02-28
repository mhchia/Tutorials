# Exercise Z3

- [x] Follow the [Z3 Playground](https://jfmc.github.io/z3-play/) up to Bitvectors (don't read Bitvectors).

> :warning: Some browsers might not run the playground properly. Safari is a browser we know doesn't work well. Chrome, Chromium, Firefox, and Brave browsers have been tested to work fine.

- [x] Use Z3 to find a solution for the following puzzle:
</br>
<img src="images/Logic_Puzzle1.png" width="350">

```z3
(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(assert (= (+ a a) 10))
(assert (= (+(* a b) b) 12))
(assert (= (- (* a b) (* c a)) a))
(check-sat)
(get-model)
```
The answer is the result of `c`, i.e. `1`.

- [x] Write a formula to check if the following two equations are equivalent:
</br>
<img src="images/Logic_Puzzle2.png" width="350">

```z3
(declare-const p Bool)
(declare-const q Bool)

; to check if the equations are equivalent
;   1. (p and q) = p
;   2. p => q
; we can see if (1) = (2) is valid.
; let conjecture = ((1) = (2)).
; conjecture is valid iff conjecture is not unsatisfiable.
(define-fun conjecture() Bool
    (= (= (and p q) p) (=> p q))
)

(assert (not conjecture))
(check-sat)
```
Result is `unsat` which implies `((p and q) = p) == (p => q)` is valid and always true, and the equations are equivalent.

- [x] A good additional practice will be to try and prove questions in [this file](AdditionalExerciseForSMT.pdf)
1. D, because all of the expressions and (= (=> p => q) false are not valid.
```z3
(declare-const p Bool)
(declare-const q Bool)

; A
(push)
(define-fun conjecture() Bool
    (and
        (and (not p) (not q))
        (= (=> p q) false)
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; B
(push)
(define-fun conjecture() Bool
    (and
        (and p q)
        (= (=> p q) false)
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; C
(push)
(define-fun conjecture() Bool
    (and
        (and (not p) q)
        (= (=> p q) false)
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions
```
2. C, because both `(= (=> (or p q) p) true)` and `(= (=> (or p q) p) false)` are not valid.

```z3
(declare-const p Bool)
(declare-const q Bool)

; is true
(push)
(define-fun conjecture() Bool
    (= (=> (or p q) p) true)
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; is false
(push)
(define-fun conjecture() Bool
    (= (=> (or p q) p) false)
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions
```

3. B, because the `expression = false` is valid, i.e. `not conjecture` is unsatisfiable.

```z3
(declare-const p Bool)
(declare-const q Bool)

; is true
(push)
(define-fun conjecture() Bool
    (=
        (and (and p (or q (not p))) (not q))
        true
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; is false
(push)
(define-fun conjecture() Bool
    (=
        (and (and p (or q (not p))) (not q))
        false
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions
```

4. A, since the `expression = true` is valid

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)


; is true
(push)
(define-fun conjecture() Bool
    (=
        (= (not (or (or (not p) (not q)) (not r))) (and (and p q) r))
        true
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; is false
(push)
(define-fun conjecture() Bool
    (=
        (= (not (or (or (not p) (not q)) (not r))) (and (and p q) r))
        false
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions
```

5. C, since both `expression = true` and `expression = false` are not valid.
```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)

; is true
(push)
(define-fun conjecture() Bool
    (=
        (not (and (or (not p) q ) (or p (not q) ) ) )
        true
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; is false
(push)
(define-fun conjecture() Bool
    (=
        (not (and (or (not p) q ) (or p (not q) ) ) )
        false
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

```

6. C, since both `expression = true` and `expression = false` are not valid.
```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)

; is true
(push)
(define-fun conjecture() Bool
    (=
        (not (or (and p q ) (and (not p) (not q) ) ) )
        true
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; is false
(push)
(define-fun conjecture() Bool
    (=
        (not (or (and p q ) (and (not p) (not q) ) ) )
        false
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

```

7. ABCD, since all `expression => p or (not p)` are valid.
```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)

; A
(push)
(define-fun conjecture() Bool
    (=>
        (or p (not p) )
        (or p (not p))
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; B
(push)
(define-fun conjecture() Bool
    (=>
        (and p (not p) )
        (or p (not p))
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; C
(push)
(define-fun conjecture() Bool
    (=>
        (or (and p (not p) ) (not p) )
        (or p (not p))
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; D
(push)
(define-fun conjecture() Bool
    (=>
        (and (or (not p) p ) (not p) )
        (or p (not p))
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions
```

8. ABCD, since all `(p and (not p)) => expression` are valid.

```
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)

; A
(push)
(define-fun conjecture() Bool
    (=>
        (and p (not p))
        (or p (not p) )
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; B
(push)
(define-fun conjecture() Bool
    (=>
        (and p (not p))
        (and p (not p) )
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; C
(push)
(define-fun conjecture() Bool
    (=>
        (and p (not p))
        (or (and p (not p) ) (not p) )
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; D
(push)
(define-fun conjecture() Bool
    (=>
        (and p (not p) )
        (and (or (not p) p ) (not p) )
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

```
9. C, since `expression = true` and `expression = false` are not valid.

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)

; is true
(push)
(define-fun conjecture() Bool
    (=
        (=> (=> p (=> q r ) ) (=> (=> p q) r ) )
        true
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; is false
(push)
(define-fun conjecture() Bool
    (=
        (=> (=> p (=> q r ) ) (=> (=> p q) r ) )
        false
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

```

10. A, since `expression = true` is valid.

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)

; is true
(push)
(define-fun conjecture() Bool
    (=
        (=> (=> (=> p q) r ) (=> p (=> q r ) ) )
        true
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

; is false
(push)
(define-fun conjecture() Bool
    (=
        (=> (=> (=> p q) r ) (=> p (=> q r ) ) )
        false
    )
)
(assert (not conjecture))
(check-sat)
(pop) ; remove the previous assertions

```

> :information_source: You might find the [cheat sheet](Cheat_Sheet.md) useful for the exercises and additional explanations of the Z3 principles.
