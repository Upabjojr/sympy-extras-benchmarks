%------------------------------------------------------------------------------
% File     : ARI733_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Real inequation system has a solution with integer X
% Version  : Especial.
% English  :

% Refs     : [Wal14] Waldmann (2014), Email to Geoff Sutcliffe
% Source   : [Wal14]
% Names    : 

% Status   : Theorem
% Rating   : 0.50 v9.1.0, 0.60 v9.0.0, 0.50 v7.5.0, 0.40 v7.4.0, 0.67 v7.3.0, 0.75 v7.1.0, 0.67 v7.0.0, 0.83 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   3   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   18 (   4 atm;   6 fun;   6 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 1-2 aty)
%            Number of functors    :    8 (   0 usr;   6 con; 0-2 aty)
%            Number of variables   :    2 (   0   !;   2   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(prove,conjecture,
    ? [X: $real,Y: $real] :
      ( $is_int(X)
      & $lesseq($sum($product(-1.5,X),Y),0.25)
      & $lesseq($sum($product(4.0,X),Y),30.5)
      & $lesseq($sum(X,$product(-2.5,Y)),-13.0) ) ).

%------------------------------------------------------------------------------
