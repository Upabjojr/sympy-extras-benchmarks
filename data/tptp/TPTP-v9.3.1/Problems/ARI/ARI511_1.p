%------------------------------------------------------------------------------
% File     : ARI511_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Mixed: 5/19 coerced to rational is less than something
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.25 v9.1.0, 0.20 v9.0.0, 0.25 v8.2.0, 0.33 v7.5.0, 0.40 v7.4.0, 0.33 v7.3.0, 0.25 v7.1.0, 0.33 v7.0.0, 0.17 v6.4.0, 0.00 v6.3.0, 0.25 v6.2.0, 0.60 v6.1.0, 0.78 v6.0.0, 0.75 v5.5.0, 0.62 v5.4.0, 0.75 v5.3.0, 0.71 v5.2.0, 0.80 v5.1.0, 1.00 v5.0.0
% Syntax   : Number of formulae    :    1 (   1 unt;   0 typ;   0 def)
%            Number of atoms       :    1 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    2 (   2 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    4 (   1 atm;   1 fun;   1 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    2 (   0 usr;   1 con; 0-1 aty)
%            Number of variables   :    1 (   0   !;   1   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(mixed_types_problem_16,conjecture,
    ? [Y: $rat] : $less($to_rat(5/19),Y) ).

%------------------------------------------------------------------------------
