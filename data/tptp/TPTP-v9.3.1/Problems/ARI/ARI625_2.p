%------------------------------------------------------------------------------
% File     : ARI625_2 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : There is no enumeration of the reals
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : CounterSatisfiable
% Rating   : 1.00 v6.2.0, 0.33 v6.0.0, 1.00 v5.3.0, 0.67 v5.2.0, 1.00 v5.1.0
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
% SPC      : TF0_CSA_EQU_ARI_NDT

% Comments : Countersatisfiable for $rat (interpret f by an enumeration 
%            of $rat).
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $rat > $rat ).

tff(not_ex_enum_of_rats,conjecture,
    ~ ! [X: $rat,Y: $rat] :
        ( ( X = Y )
        | $less(f(X),f(Y))
        | $greatereq(f(X),$sum(f(Y),1/1)) ) ).

%------------------------------------------------------------------------------
