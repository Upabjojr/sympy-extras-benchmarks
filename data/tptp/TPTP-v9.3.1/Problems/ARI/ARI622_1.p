%------------------------------------------------------------------------------
% File     : ARI622_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : There exist two powers of 2 whose sum equals 10
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v7.5.0, 0.30 v7.4.0, 0.25 v7.3.0, 0.00 v7.0.0, 0.14 v6.4.0, 0.00 v6.3.0, 0.14 v6.2.0, 0.50 v6.1.0, 0.67 v6.0.0, 0.71 v5.5.0, 0.78 v5.4.0, 0.88 v5.3.0, 0.80 v5.2.0, 0.83 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    8 (   3 equ)
%            Maximal formula atoms :    8 (   8 avg)
%            Number of connectives :    7 (   0   ~;   1   |;   4   &)
%                                         (   1 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    8 (   8 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   11 (   1 atm;   2 fun;   4 num;   4 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   1 usr;   0 prp; 1-2 aty)
%            Number of functors    :    5 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    4 (   1   !;   3   ?;   4   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : Also a theorem for $rat and $real
%------------------------------------------------------------------------------
tff(pow2_type,type,
    pow2: $int > $o ).

tff(sum_of_pows_of_2_eq_10,conjecture,
    ( ! [X: $int] :
        ( pow2(X)
      <=> ( ( X = 1 )
          | ( $lesseq(2,X)
            & ? [Y: $int] :
                ( ( $product(2,Y) = X )
                & pow2(Y) ) ) ) )
   => ? [X: $int,Y: $int] :
        ( pow2(X)
        & pow2(Y)
        & ( $sum(X,Y) = 10 ) ) ) ).

%------------------------------------------------------------------------------
