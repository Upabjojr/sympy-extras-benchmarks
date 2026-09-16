%------------------------------------------------------------------------------
% File     : ARI741_1 : TPTP v9.3.1. Released v7.0.0.
% Domain   : Arithmetic
% Problem  : Real power of real
% Version  : Especial.
% English  :

% Refs     : [Pas16] Paskevich (2016), Email to Geoff Sutcliffe
% Source   : [Pas16]
% Names    : real-PowerRealTest-Pow_2_2.p [Pas16]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v8.2.0, 0.25 v8.1.0, 0.38 v7.5.0, 0.30 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0
% Syntax   : Number of formulae    :   31 (   9 unt;   7 typ;   0 def)
%            Number of atoms       :   42 (  21 equ)
%            Maximal formula atoms :    3 (   1 avg)
%            Number of connectives :   18 (   0   ~;   0   |;   3   &)
%                                         (   0 <=>;  15  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   3 avg)
%            Maximal term depth    :    4 (   1 avg)
%            Number arithmetic     :  101 (  21 atm;  14 fun;  35 num;  31 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    8 (   7   >;   1   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   16 (   7 usr;   6 con; 0-2 aty)
%            Number of variables   :   31 (  31   !;   0   ?;  31   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(exp,type,
    exp: $real > $real ).

tff(exp_zero,axiom,
    exp(0.0) = 1.0 ).

tff(exp_sum,axiom,
    ! [X: $real,Y: $real] : ( exp($sum(X,Y)) = $product(exp(X),exp(Y)) ) ).

tff(log,type,
    log: $real > $real ).

tff(log_one,axiom,
    log(1.0) = 0.0 ).

tff(log_mul,axiom,
    ! [X: $real,Y: $real] :
      ( ( $less(0.0,X)
        & $less(0.0,Y) )
     => ( log($product(X,Y)) = $sum(log(X),log(Y)) ) ) ).

tff(log_exp,axiom,
    ! [X: $real] : ( log(exp(X)) = X ) ).

tff(exp_log,axiom,
    ! [X: $real] :
      ( $less(0.0,X)
     => ( exp(log(X)) = X ) ) ).

tff(log2,type,
    log2: $real > $real ).

tff(log2_def,axiom,
    ! [X: $real] : ( log2(X) = $quotient(log(X),log(2.0)) ) ).

tff(log10,type,
    log10: $real > $real ).

tff(log10_def,axiom,
    ! [X: $real] : ( log10(X) = $quotient(log(X),log(10.0)) ) ).

tff(pow,type,
    pow: ( $real * $real ) > $real ).

tff(pow_def,axiom,
    ! [X: $real,Y: $real] :
      ( $less(0.0,X)
     => ( pow(X,Y) = exp($product(Y,log(X))) ) ) ).

tff(pow_pos,axiom,
    ! [X: $real,Y: $real] :
      ( $less(0.0,X)
     => $less(0.0,pow(X,Y)) ) ).

tff(pow_plus,axiom,
    ! [X: $real,Y: $real,Z: $real] :
      ( $less(0.0,Z)
     => ( pow(Z,$sum(X,Y)) = $product(pow(Z,X),pow(Z,Y)) ) ) ).

tff(pow_mult,axiom,
    ! [X: $real,Y: $real,Z: $real] :
      ( $less(0.0,X)
     => ( pow(pow(X,Y),Z) = pow(X,$product(Y,Z)) ) ) ).

tff(pow_x_zero,axiom,
    ! [X: $real] :
      ( $less(0.0,X)
     => ( pow(X,0.0) = 1.0 ) ) ).

tff(pow_x_one,axiom,
    ! [X: $real] :
      ( $less(0.0,X)
     => ( pow(X,1.0) = X ) ) ).

tff(pow_one_y,axiom,
    ! [Y: $real] : ( pow(1.0,Y) = 1.0 ) ).

tff(sqr,type,
    sqr: $real > $real ).

tff(sqr_def,axiom,
    ! [X: $real] : ( sqr(X) = $product(X,X) ) ).

tff(sqrt,type,
    sqrt: $real > $real ).

tff(sqrt_positive,axiom,
    ! [X: $real] :
      ( $lesseq(0.0,X)
     => $lesseq(0.0,sqrt(X)) ) ).

tff(sqrt_square,axiom,
    ! [X: $real] :
      ( $lesseq(0.0,X)
     => ( sqr(sqrt(X)) = X ) ) ).

tff(square_sqrt,axiom,
    ! [X: $real] :
      ( $lesseq(0.0,X)
     => ( sqrt($product(X,X)) = X ) ) ).

tff(sqrt_mul,axiom,
    ! [X: $real,Y: $real] :
      ( ( $lesseq(0.0,X)
        & $lesseq(0.0,Y) )
     => ( sqrt($product(X,Y)) = $product(sqrt(X),sqrt(Y)) ) ) ).

tff(sqrt_le,axiom,
    ! [X: $real,Y: $real] :
      ( ( $lesseq(0.0,X)
        & $lesseq(X,Y) )
     => $lesseq(sqrt(X),sqrt(Y)) ) ).

tff(pow_x_two,axiom,
    ! [X: $real] :
      ( $less(0.0,X)
     => ( pow(X,2.0) = sqr(X) ) ) ).

tff(pow_half,axiom,
    ! [X: $real] :
      ( $less(0.0,X)
     => ( pow(X,0.5) = sqrt(X) ) ) ).

tff(pow_2_21,conjecture,
    pow(2.0,2.0) = 4.0 ).

%------------------------------------------------------------------------------
