%------------------------------------------------------------------------------
% File     : ARI557_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Rational: Product something and 9/12 is 3/7 means 1/2 less than it
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v9.1.0, 0.25 v9.0.0, 0.12 v8.2.0, 0.25 v8.1.0, 0.38 v7.5.0, 0.30 v7.4.0, 0.25 v7.3.0, 0.33 v7.1.0, 0.50 v7.0.0, 0.14 v6.4.0, 0.00 v6.3.0, 0.14 v6.2.0, 0.62 v6.1.0, 0.44 v6.0.0, 0.29 v5.5.0, 0.56 v5.4.0, 0.38 v5.3.0, 0.50 v5.2.0, 0.33 v5.1.0, 0.40 v5.0.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   1 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    6 (   1 atm;   1 fun;   3 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    1 (   0   !;   1   ?;   1   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(rat_combined_problem_17,conjecture,
    ? [X: $rat] :
      ( ( $product(X,9/12) = 3/7 )
      & $less(1/2,X) ) ).

%------------------------------------------------------------------------------
