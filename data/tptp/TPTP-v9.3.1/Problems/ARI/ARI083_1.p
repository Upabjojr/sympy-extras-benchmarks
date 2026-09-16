%------------------------------------------------------------------------------
% File     : ARI083_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Associative sum exists
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.00 v6.2.0, 0.25 v6.1.0, 0.11 v6.0.0, 0.14 v5.5.0, 0.11 v5.4.0, 0.12 v5.3.0, 0.20 v5.2.0, 0.17 v5.1.0, 0.20 v5.0.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    5 (   5 equ)
%            Maximal formula atoms :    5 (   5 avg)
%            Number of connectives :    4 (   0   ~;   0   |;   3   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :   12 (  12 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   11 (   0 atm;   4 fun;   0 num;   7 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    1 (   0 usr;   0 con; 2-2 aty)
%            Number of variables   :    7 (   0   !;   7   ?;   7   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(associative_sum_exists,conjecture,
    ? [X: $int,Y: $int,Z: $int,Z1: $int,Z2: $int,Z3: $int,Z4: $int] :
      ( ( ( $sum(X,Y) = Z1 )
        & ( $sum(Z1,Z) = Z2 )
        & ( $sum(Y,Z) = Z3 )
        & ( $sum(X,Z3) = Z4 ) )
     => ( Z2 = Z4 ) ) ).

%------------------------------------------------------------------------------
