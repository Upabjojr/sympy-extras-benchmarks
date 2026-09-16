%------------------------------------------------------------------------------
% File     : ARI625_1 : TPTP v9.3.1. Bugfixed v5.2.0.
% Domain   : Arithmetic
% Problem  : There is no enumeration of the reals
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 1.00 v5.2.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    3 (   1 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    3 (   1   ~;   2   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    6 (   2 atm;   1 fun;   1 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    3 (   1 usr;   1 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : Countersatisfiable for $rat (interpret f by an enumeration 
%            of $rat).
% Bugfixes : v5.2.0 - Made numbers into reals.
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $real > $real ).

tff(not_ex_enum_of_reals,conjecture,
    ~ ! [X: $real,Y: $real] :
        ( ( X = Y )
        | $less(f(X),f(Y))
        | $greatereq(f(X),$sum(f(Y),1.0)) ) ).

%------------------------------------------------------------------------------
