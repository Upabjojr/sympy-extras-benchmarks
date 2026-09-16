%------------------------------------------------------------------------------
% File     : ARI400_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Real: Something is not 20.06
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.25 v9.1.0, 0.38 v9.0.0, 0.25 v8.1.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.38 v7.3.0, 0.50 v7.0.0, 0.14 v6.4.0, 0.00 v6.3.0, 0.43 v6.2.0, 0.38 v6.1.0, 0.33 v6.0.0, 0.29 v5.5.0, 0.44 v5.4.0, 0.38 v5.3.0, 0.60 v5.2.0, 0.67 v5.1.0, 0.80 v5.0.0
% Syntax   : Number of formulae    :    1 (   1 unt;   0 typ;   0 def)
%            Number of atoms       :    1 (   1 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    1 (   1   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    1 (   1 avg)
%            Number arithmetic     :    2 (   0 atm;   0 fun;   1 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    1 (   0 usr;   1 con; 0-0 aty)
%            Number of variables   :    1 (   0   !;   1   ?;   1   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(real_not_equal_problem_2,conjecture,
    ? [X: $real] : ( X != 20.06 ) ).

%------------------------------------------------------------------------------
