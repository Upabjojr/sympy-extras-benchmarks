%------------------------------------------------------------------------------
% File     : ARI525_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Mixed: ((- 7/15) + 4/15) coerced to integer is greatereq to 0
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : CounterSatisfiable
% Rating   : 0.00 v6.3.0, 0.25 v6.2.0, 0.60 v6.1.0, 0.67 v6.0.0, 0.88 v5.4.0, 0.75 v5.3.0, 0.71 v5.2.0
% Syntax   : Number of formulae    :    1 (   1 unt;   0 typ;   0 def)
%            Number of atoms       :    1 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :    7 (   1 atm;   3 fun;   3 num;   0 var)
%            Number of types       :    0 (   0 usr)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_CSA_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(mixed_types_problem_30,conjecture,
    $greatereq($to_int($sum($uminus(7/15),4/15)),0) ).

%------------------------------------------------------------------------------
