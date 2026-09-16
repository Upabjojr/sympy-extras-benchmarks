%------------------------------------------------------------------------------
% File     : ARI082_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Associative sum
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.00 v6.2.0, 0.12 v6.1.0, 0.11 v6.0.0, 0.00 v5.3.0, 0.10 v5.2.0, 0.17 v5.1.0, 0.20 v5.0.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    5 (   5 equ)
%            Maximal formula atoms :    5 (   5 avg)
%            Number of connectives :    4 (   0   ~;   0   |;   3   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    9 (   9 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   14 (   0 atm;   4 fun;   6 num;   4 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    4 (   4   !;   0   ?;   4   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(associative_sum,conjecture,
    ! [Z1: $int,Z2: $int,Z3: $int,Z4: $int] :
      ( ( ( $sum(2,3) = Z1 )
        & ( $sum(Z1,6) = Z2 )
        & ( $sum(3,6) = Z3 )
        & ( $sum(2,Z3) = Z4 ) )
     => ( Z2 = Z4 ) ) ).

%------------------------------------------------------------------------------
