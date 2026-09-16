%------------------------------------------------------------------------------
% File     : ARI717_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : floor(X+0.5) can be greater than X
% Version  : Especial.
% English  :

% Refs     : [Wal14] Waldmann (2014), Email to Geoff Sutcliffe
% Source   : [Wal14]
% Names    : 

% Status   : Theorem
% Rating   : 0.00 v9.1.0, 0.20 v9.0.0, 0.00 v7.4.0, 0.17 v7.3.0, 0.25 v7.1.0, 0.17 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    1 (   1 unt;   0 typ;   0 def)
%            Number of atoms       :    1 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    2 (   2 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    5 (   1 atm;   2 fun;   1 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    3 (   0 usr;   1 con; 0-2 aty)
%            Number of variables   :    1 (   0   !;   1   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(prove,conjecture,
    ? [X: $real] : $greater($floor($sum(X,0.5)),X) ).

%------------------------------------------------------------------------------
