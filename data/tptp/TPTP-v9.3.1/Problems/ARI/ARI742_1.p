%------------------------------------------------------------------------------
% File     : ARI742_1 : TPTP v9.3.1. Released v7.0.0.
% Domain   : Arithmetic
% Problem  : Square root of 0.0
% Version  : Especial.
% English  :

% Refs     : [Pas16] Paskevich (2016), Email to Geoff Sutcliffe
% Source   : [Pas16]
% Names    : real-SquareTest-Sqrt_zero.p [Pas16]

% Status   : Theorem
% Rating   : 0.00 v8.1.0, 0.12 v7.5.0, 0.20 v7.4.0, 0.25 v7.3.0, 0.33 v7.0.0
% Syntax   : Number of formulae    :    9 (   2 unt;   2 typ;   0 def)
%            Number of atoms       :   14 (   5 equ)
%            Maximal formula atoms :    3 (   2 avg)
%            Number of connectives :    7 (   0   ~;   0   |;   2   &)
%                                         (   0 <=>;   5  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   3 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   30 (   9 atm;   4 fun;   9 num;   8 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   2   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   2 usr;   1 con; 0-2 aty)
%            Number of variables   :    8 (   8   !;   0   ?;   8   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
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

tff(sqrt_zero,conjecture,
    sqrt(0.0) = 0.0 ).

%------------------------------------------------------------------------------
