%------------------------------------------------------------------------------
% File     : ARI162_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Sum is 8 and difference is 0
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v9.1.0, 0.25 v9.0.0, 0.12 v8.2.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.25 v7.3.0, 0.17 v7.0.0, 0.29 v6.4.0, 0.00 v6.3.0, 0.43 v6.2.0, 0.62 v6.1.0, 0.56 v6.0.0, 0.57 v5.5.0, 0.56 v5.4.0, 0.62 v5.3.0, 0.60 v5.2.0, 0.67 v5.1.0, 0.80 v5.0.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   2 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    6 (   0 atm;   2 fun;   2 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    2 (   0   !;   2   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(sum_and_difference,conjecture,
    ? [X: $int,Y: $int] :
      ( ( $sum(X,Y) = 8 )
      & ( $difference(X,Y) = 0 ) ) ).

%------------------------------------------------------------------------------
