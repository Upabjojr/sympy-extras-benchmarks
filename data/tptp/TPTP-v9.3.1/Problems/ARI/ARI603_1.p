%------------------------------------------------------------------------------
% File     : ARI603_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : If f(X) > X, then Y = Z + (Y-Z) < Z + f(Y-Z)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.25 v9.1.0, 0.40 v9.0.0, 0.25 v8.2.0, 0.33 v7.5.0, 0.40 v7.4.0, 0.33 v7.3.0, 0.38 v7.1.0, 0.33 v7.0.0, 0.17 v6.4.0, 1.00 v6.3.0, 0.75 v6.2.0, 0.60 v6.1.0, 0.67 v6.0.0, 0.62 v5.5.0, 0.50 v5.4.0, 0.75 v5.3.0, 0.86 v5.2.0, 1.00 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    7 (   2 atm;   1 fun;   0 num;   4 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    2 (   1 usr;   0 con; 1-2 aty)
%            Number of variables   :    4 (   3   !;   1   ?;   4   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(fX_gt_X_implies_exist_large_fX,conjecture,
    ( ! [X: $int] : $greater(f(X),X)
   => ! [Y: $int,Z: $int] :
      ? [X: $int] : $less(Y,$sum(Z,f(X))) ) ).

%------------------------------------------------------------------------------
