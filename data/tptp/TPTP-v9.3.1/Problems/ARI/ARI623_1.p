%------------------------------------------------------------------------------
% File     : ARI623_1 : TPTP v9.3.1. Bugfixed v5.2.0.
% Domain   : Arithmetic
% Problem  : There is no strictly mon fct from $rat or $real to a non-dense set
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 1.00 v5.2.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    2 (   1   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    6 (   2 atm;   1 fun;   1 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    3 (   1 usr;   1 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : Also a theorem for $real (but countersatisfiable in ordered 
%            divisible abelian groups).
% Bugfixes : v5.2.0 - Made numbers into rationals.
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $rat > $rat ).

tff(not_ex_mon_mapping_rat_to_nondense,conjecture,
    ~ ! [X: $rat,Y: $rat] :
        ( $greater(X,Y)
       => $greater(f(X),$sum(f(Y),1/1)) ) ).

%------------------------------------------------------------------------------
