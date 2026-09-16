%------------------------------------------------------------------------------
% File     : ARI604_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : If f(X) > X, then f(-X) > -X, hence -f(-X) < X < f(X)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.33 v6.0.0, 0.38 v5.4.0, 0.62 v5.3.0, 0.71 v5.2.0, 0.80 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :    6 (   2 atm;   2 fun;   0 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    2 (   1 usr;   0 con; 1-1 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(fX_gt_X_implies_negfnegX_lt_fX,conjecture,
    ( ! [X: $int] : $greater(f(X),X)
   => ! [X: $int] : $less($uminus(f($uminus(X))),f(X)) ) ).

%------------------------------------------------------------------------------
