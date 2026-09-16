%------------------------------------------------------------------------------
% File     : ARI744_1 : TPTP v9.3.1. Released v7.0.0.
% Domain   : Arithmetic
% Problem  : Square root of real
% Version  : Especial.
% English  :

% Refs     : [Pas16] Paskevich (2016), Email to Geoff Sutcliffe
% Source   : [Pas16]
% Names    : real-SquareTest-Sqrt_four.p [Pas16]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.38 v9.1.0, 0.50 v9.0.0, 0.38 v7.5.0, 0.50 v7.1.0, 0.67 v7.0.0
% Syntax   : Number of formulae    :   11 (   4 unt;   2 typ;   0 def)
%            Number of atoms       :   16 (   7 equ)
%            Maximal formula atoms :    3 (   1 avg)
%            Number of connectives :    7 (   0   ~;   0   |;   2   &)
%                                         (   0 <=>;   5  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   3 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   34 (   9 atm;   4 fun;  13 num;   8 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   2   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    7 (   2 usr;   4 con; 0-2 aty)
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

tff(sqrt_zero,axiom,
    sqrt(0.0) = 0.0 ).

tff(sqrt_one,axiom,
    sqrt(1.0) = 1.0 ).

tff(sqrt_four,conjecture,
    sqrt(4.0) = 2.0 ).

%------------------------------------------------------------------------------
