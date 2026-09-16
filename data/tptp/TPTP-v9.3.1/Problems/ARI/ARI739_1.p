%------------------------------------------------------------------------------
% File     : ARI739_1 : TPTP v9.3.1. Released v7.0.0.
% Domain   : Arithmetic
% Problem  : Log of exponent of 1.0
% Version  : Especial.
% English  :

% Refs     : [Pas16] Paskevich (2016), Email to Geoff Sutcliffe
% Source   : [Pas16]
% Names    : real-ExpLogTest-Log_e.p [Pas16]

% Status   : Theorem
% Rating   : 0.00 v8.2.0, 0.12 v8.1.0, 0.25 v7.5.0, 0.20 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0
% Syntax   : Number of formulae    :   13 (   7 unt;   4 typ;   0 def)
%            Number of atoms       :   12 (   9 equ)
%            Maximal formula atoms :    3 (   1 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   2 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :   28 (   3 atm;   6 fun;  11 num;   8 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    4 (   4   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   11 (   4 usr;   4 con; 0-2 aty)
%            Number of variables   :    8 (   8   !;   0   ?;   8   :)
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

tff(log_e,conjecture,
    log(exp(1.0)) = 1.0 ).

%------------------------------------------------------------------------------
